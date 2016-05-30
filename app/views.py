from flask import render_template, jsonify
from flask_classy import FlaskView, request, route
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, BodySizeForm, EditExercise, RepeatForm
from app.models import User, BodySize, Sets, Repeats, Categories
from functools import wraps
from datetime import datetime
from collections import defaultdict
import trafaret as t
import calendar


def check_login(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            response = jsonify(auth='Вы уже авторизованы')
            response.status_code = 409
            return response
        return func(*args, **kwargs)
    return decorated_view


@app.route('/')
def index():
    return render_template('main.html')


class AccountView(FlaskView):
    @route('/registration/', methods=['POST'])
    @check_login
    def registration(self):
        form = RegistrationForm(data=request.get_json())
        if form.validate():
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=bcrypt.generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            return '', 201
        response = jsonify(error='Что-то пошло не так. Попробуйте позже.')
        response.status_code = 404
        return response

    @route('/login/', methods=['POST'])
    @check_login
    def login(self):
        form = LoginForm(data=request.get_json())
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                response = jsonify(error='Пользователь не найден')
                response.status_code = 404
                return response
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return '', 200
            response = jsonify(error='Не правильно введен логин или пароль')
            response.status_code = 404
            return response

    @login_required
    def logout(self):
        logout_user()
        return '', 200

    @login_required
    def check_auth(self):
        return '', 200

    @route('/check_unique/', methods=['POST'])
    def check_unique(self):
        data = request.get_json()
        unique = None
        if 'username' in data:
            unique = User.query.filter_by(username=data['username']).first()
        elif 'email' in data:
            unique = User.query.filter_by(email=data['email']).first()
        if not unique:
            return '', 200
        return '', 404


class SetsView(FlaskView):
    decorators = [login_required]

    def index(self):
        out_data = defaultdict(list)
        dates = get_dates(datetime.today().month, datetime.today().year)
        sets = [day.serialize for day in current_user.sets.filter(Sets.date >= dates['start'],
                                                                  Sets.date <= dates['end']).all()]
        for item in sets:
            out_data[item['date']].append(item)
        return jsonify(sets=out_data)

    def get(self, id):
        one_set = current_user.sets.filter(Sets.id == id).first()
        return jsonify(set=one_set.serialize)

    @route('/<month>/<year>', methods=['GET'])
    def sets_for_months(self, month, year):
        dates = get_dates(month, year)
        out_data = defaultdict(list)
        sets = [day.serialize for day in current_user.sets.filter(Sets.date >= dates['start'],
                                                                  Sets.date <= dates['end']).all()]
        for item in sets:
            out_data[item['date']].append(item)
        return jsonify(sets=out_data)

    @route('/by_date/<date>', methods=['GET'])
    def sets_by_date(self, date):
        out_data = defaultdict(list)
        day=[day.serialize for day in current_user.sets.filter(
            Sets.date == datetime.strptime(date, '%Y-%m-%d')).all()]
        for item in day:
            out_data[item['date']].append(item)
        return jsonify(day=out_data)

    def post(self):
        t_set = t.Dict({
            t.Key('date') >> 'date': t.String,
            t.Key('exercise') >> 'exercise': t.Int,
            t.Key('exercise_name', optional=True) >> 'exercise_name': t.String,
            t.Key('repeats') >> 'repeats': t.List(
                t.Mapping(
                    t.String, t.Float
                )
            )
        })
        data = request.get_json()
        print(data)
        for day in data:
            try:
                day_check = t_set.check(day)
                sets = Sets(
                    date=datetime.strptime(day_check['date'], '%Y-%m-%d'),
                    exercise_id=day_check['exercise'],
                    user_id=current_user.id
                )
                db.session.add(sets)
                db.session.flush()
                for repeat in day_check['repeats']:
                    repeat_instance = Repeats(
                        set_id=sets.id,
                        weight=repeat['weight'],
                        repeat=repeat['repeats'],
                    )
                    db.session.add(repeat_instance)
                    db.session.flush()
            except t.DataError as e:
                print(e)
                return '', 404
        db.session.commit()
        return '', 201

    def patch(self, id):
        form = EditExercise(data=request.get_json())
        if form.validate():
            Sets.query.filter_by(id=int(id)).update({
                'exercise_id': form.exercise.data
            })
            db.session.commit()
            return '', 200
        return '', 404

    def delete(self, id):
        print(id)
        exercise = Sets.query.get(int(id))
        db.session.delete(exercise)
        try:
            db.session.commit()
        except Exception:
            response = jsonify(error='Произошла ошибка. Попробуйте позже')
            response.status_code = 404
            return response
        return '', 200


class RepeatsView(FlaskView):
    decorators = [login_required]

    def get(self, id):
        repeat = Repeats.query.get(int(id))
        return jsonify(repeat=repeat.serialize)

    def post(self):
        form = RepeatForm(data=request.get_json())
        if form.validate():
            repeats = Repeats(
                set_id=form.set.data,
                weight=form.weight.data,
                repeat=form.repeats.data,
            )
            db.session.add(repeats)
            db.session.commit()
            return '', 201
        return 409

    def patch(self, id):
        form = RepeatForm(data=request.get_json())
        if form.validate():
            Repeats.query.filter_by(id=int(id)).update({
                'set_id': form.set.data,
                'weight': form.weight.data,
                'repeat': form.repeats.data
            })
            db.session.commit()
            return '', 200
        return '', 409

    def delete(self, id):
        r = Repeats.query.get(int(id))
        db.session.delete(r)
        try:
            db.session.commit()
        except Exception:
            response = jsonify(error='Произошла ошибка. Попробуйте позже')
            response.status_code = 404
            return response
        return '', 200


class CategoriesView(FlaskView):
    decorators = [login_required]

    def index(self):
        return jsonify(categories=[cat.serialize for cat in Categories.query.all()])


class ExercisesView(FlaskView):
    decorators = [login_required]

    @route('/exercises_by_category/<id>', methods=['GET'])
    def exercises_by_category(self, id):
        category = Categories.query.get(int(id))
        return jsonify(exercises=[exercise.serialize for exercise in category.exercises.all()])


class ProfileView(FlaskView):
    decorators = [login_required]

    def index(self):
        return jsonify(current_user.serialize)

    def change_password(self):
        pass


class BodysizeView(FlaskView):
    decorators = [login_required]

    def index(self):
        return jsonify(body_size=[bs.serialize for bs in BodySize.query.order_by(desc(BodySize.date)).limit(10).all()])

    def get(self, id):
        body_size = BodySize.query.get(int(id))
        return jsonify(body_size=body_size.serialize)

    def patch(self, id):
        form = BodySizeForm(data=request.get_json())
        if form.validate():
            BodySize.query.filter_by(id=int(id)).update({
                'date': datetime.strptime(form.date.data, '%Y-%m-%d'),
                'hip': form.hip.data,
                'waist': form.waist.data,
                'chest': form.chest.data,
                'arm': form.arm.data,
                'weight': form.weight.data
            })
            db.session.commit()
            return '', 200
        response = jsonify(error='Не верно введенеы данные. Попробуйте снова.')
        response.status_code = 409
        return response

    def post(self):
        form = BodySizeForm(data=request.get_json())
        if form.validate():
            body_ize = BodySize(
                date=form.date.data,
                chest=form.chest.data,
                waist=form.waist.data,
                hip=form.hip.data,
                arm=form.arm.data,
                weight=form.weight.data,
                user_id=current_user.id
            )
            db.session.add(body_ize)
            db.session.commit()
            return '', 201
        response = jsonify(error='Не верно введенеы данные. Попробуйте снова.')
        response.status_code = 409
        return response

    def delete(self, id):
        body_size = BodySize.query.get(int(id))
        db.session.delete(body_size)
        try:
            db.session.commit()
        except Exception:
            response = jsonify(error='Произошла ошибка. Попробуйте позже')
            response.status_code = 404
            return response
        return '', 200


def get_dates(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    start = datetime(year=int(year), month=int(month), day=1)
    end = datetime(year=int(year), month=int(month), day=last_day)
    return {'start': start, 'end': end}
