import trafaret as t
import calendar

from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, BodySizeForm, EditExercise, RepeatForm
from app.models import User, BodySize, Sets, Repeats, Categories
from collections import defaultdict
from datetime import datetime
from flask import render_template, jsonify
from flask_classy import FlaskView, request, route
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError


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
        form = RegistrationForm(data=request.get_json(force=True))
        if form.validate():
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=bcrypt.generate_password_hash(form.password.data)
            )
            try:
                db.session.add(user)
                db.session.commit()
                return '', 201
            except SQLAlchemyError as e:
                # TODO: loging exeption e
                db.session.rollback()
                return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        return return_response(404, jsonify(error='Не вверно введены данные.'))

    @route('/login/', methods=['POST'])
    @check_login
    def login(self):
        form = LoginForm(data=request.get_json(force=True))
        if form.validate():
            try:
                user = User.query.filter_by(username=form.username.data).first()
            except SQLAlchemyError as e:
                # TODO: loging exeption e
                return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
            if user is None:
                return return_response(404, jsonify(error='Пользователь не найден'))
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return '', 200
            return return_response(404, jsonify(error='Не правильно введен логин или пароль'))

    @login_required
    def logout(self):
        logout_user()
        return '', 200

    @login_required
    def check_auth(self):
        return '', 200

    @route('/check_unique/', methods=['POST'])
    def check_unique(self):
        data = request.get_json(force=True)
        unique = None
        if 'username' in data:
            unique = User.query.filter_by(username=data['username']).first()
        elif 'email' in data:
            unique = User.query.filter_by(email=data['email']).first()
        if not unique:
            return '', 200
        return '', 404

    @route('/change_password/', methods=['POST'])
    @login_required
    def change_password(self):
        data = request.get_json(force=True)
        if not bcrypt.check_password_hash(current_user.password, data['old']):
            return return_response(404, jsonify(error='Старый пароль введен не верно'))
        if not data['new'] == data['confirm']:
            return return_response(404, jsonify(error='Новый пароль и подтверждение пароля не совпадают'))
        try:
            User.query.filter_by(id=current_user.id).update({
                'password': bcrypt.generate_password_hash(data['new'])
            })
            db.session.commit()
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        return '', 200


class SetsView(FlaskView):

    decorators = [login_required]

    def index(self):
        out_data = defaultdict(list)
        dates = get_dates(datetime.today().month, datetime.today().year)
        try:
            sets = [day.serialize for day in current_user.sets.filter(Sets.date >= dates['start'],
                                                                      Sets.date <= dates['end']).all()]
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        for item in sets:
            out_data[item['date']].append(item)
        return jsonify(sets=out_data)

    def get(self, id):
        try:
            one_set = current_user.sets.filter(Sets.id == id).first()
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        return jsonify(set=one_set.serialize)

    @route('/<month>/<year>', methods=['GET'])
    def sets_for_months(self, month, year):
        dates = get_dates(month, year)
        out_data = defaultdict(list)
        try:
            sets = [day.serialize for day in current_user.sets.filter(Sets.date >= dates['start'],
                                                                      Sets.date <= dates['end']).all()]
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        for item in sets:
            out_data[item['date']].append(item)
        return jsonify(sets=out_data)

    @route('/by_date/<date>', methods=['GET'])
    def sets_by_date(self, date):
        out_data = defaultdict(list)
        try:
            day=[day.serialize for day in current_user.sets.filter(
                Sets.date == datetime.strptime(date, '%Y-%m-%d')).all()]
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
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
        data = request.get_json(force=True)
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
                return '', 404
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        return '', 201

    def patch(self, id):
        form = EditExercise(data=request.get_json())
        try:
            if form.validate():
                Sets.query.filter_by(id=int(id)).update({
                    'exercise_id': form.exercise.data
                })
                db.session.commit()
                return '', 200
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        return '', 404

    def delete(self, id):
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
        try:
            repeat = Repeats.query.get(int(id))
            s = Sets.query.get(repeat.set_id)
            if not s.user_id == current_user.id:
                return return_response(404, jsonify(error='Отказано в доступе'))
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        return jsonify(repeat=repeat.serialize)

    def post(self):
        form = RepeatForm(data=request.get_json(force=True))
        if form.validate():
            repeats = Repeats(
                set_id=form.set.data,
                weight=form.weight.data,
                repeat=form.repeats.data,
            )
            try:
                db.session.add(repeats)
                db.session.commit()
            except SQLAlchemyError as e:
                return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
            return '', 201
        return '',  409

    def patch(self, id):
        r = Repeats.query.get(int(id))
        s = Sets.query.get(r.set_id)
        if not s.user_id == current_user.id:
            return return_response(404, jsonify(error='Отказано в доступе'))
        form = RepeatForm(data=request.get_json(force=True))
        if form.validate():
            r.set_id = form.set.data
            r.weight = form.weight.data
            r.repeat = form.repeats.data
            db.session.commit()
            return '', 200
        return '', 409

    def delete(self, id):
        r = Repeats.query.get(int(id))
        s = Sets.query.get(r.set_id)
        if not s.user_id == current_user.id:
            return return_response(404, jsonify(error='Отказано в доступе'))
        db.session.delete(r)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
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


class BodysizeView(FlaskView):
    decorators = [login_required]

    def index(self):
        return jsonify(body_size=[bs.serialize for bs in BodySize.query.order_by(desc(BodySize.date)).limit(10).all()])

    def get(self, id):
        try:
            body_size = BodySize.query.get(int(id))
            if not body_size.user_id == current_user.id:
                return return_response(404, jsonify(error='Отказано в доступе'))
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        return jsonify(body_size=body_size.serialize)

    def patch(self, id):
        form = BodySizeForm(data=request.get_json(force=True))
        try:
            bs = BodySize.query.filter_by(id=int(id)).first()
            if not bs.user_id == current_user.id:
                return return_response(404, jsonify(error='Отказано в доступе'))
            if form.validate():
                bs.date = datetime.strptime(form.date.data, '%Y-%m-%d')
                bs.hip = form.hip.data
                bs.waist = form.waist.data
                bs.chest = form.chest.data
                bs.arm = form.arm.data
                bs.weight = form.weight.data
                db.session.commit()
                return '', 200
        except SQLAlchemyError as e:
            return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        response = jsonify(error='Не верно введенеы данные. Попробуйте снова.')
        response.status_code = 409
        return response

    def post(self):
        form = BodySizeForm(data=request.get_json(force=True))
        if form.validate():
            body_size = BodySize(
                date=form.date.data,
                chest=form.chest.data,
                waist=form.waist.data,
                hip=form.hip.data,
                arm=form.arm.data,
                weight=form.weight.data,
                user_id=current_user.id
            )
            try:
                db.session.add(body_size)
                db.session.commit()
                return '', 201
            except SQLAlchemyError as e:
                db.session.rollback()
                return return_response(500, jsonify(error='Произошлка ошибка во время запроса.'))
        return return_response(409, jsonify(error='Не верно введенеы данные. Попробуйте снова.'))

    def delete(self, id):
        try:
            body_size = BodySize.query.get(int(id))
            if not body_size.user_id == current_user.id:
                return return_response(404, jsonify(error='Отказано в доступе'))
            db.session.delete(body_size)
            db.session.commit()
        except SQLAlchemyError as e:
            return return_response(404, jsonify(error='Произошла ошибка. Попробуйте позже'))
        return '', 200


def get_dates(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    start = datetime(year=int(year), month=int(month), day=1)
    end = datetime(year=int(year), month=int(month), day=last_day)
    return {'start': start, 'end': end}


def return_response(status, msg):
    response = msg
    response.status_code = status
    return response
