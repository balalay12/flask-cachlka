from flask import render_template, jsonify
from flask_classy import FlaskView, request, route
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, BodySizeForm, SetsForm
from app.models import User, BodySize, Sets, Repeats, Categories, Exercise
from functools import wraps
from datetime import date


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
        else:
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
            else:
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
        else:
            return '', 404


class SetsView(FlaskView):
    @login_required
    def index(self):
        print(current_user.sets.all())
        return '', 200

    @login_required
    def post(self):
        data = request.get_json()
        for day in data:
            print('1', day)
            repeats = day.pop('repeats')
            del day['exercise_name']
            print('2', day)
            form = SetsForm(data=day)
            print('3', form.date.data, form.exercise.data)
            if form.validate():
                print('validate')
                return '', 200
            else:
                print(form.errors)
                return '', 200


class CategoriesView(FlaskView):
    @login_required
    def index(self):
        return jsonify(categories=[cat.serialize for cat in Categories.query.all()])


class ExercisesView(FlaskView):
    @route('/exercises_by_category/<id>', methods=['GET'])
    @login_required
    def exercises_by_category(self, id):
        category = Categories.query.get(int(id))
        return jsonify(exercises=[exercise.serialize for exercise in category.exercises])


class ProfileView(FlaskView):
    @login_required
    def index(self):
        return jsonify(current_user.serialize)

    @login_required
    def change_password(self):
        pass


class BodysizeView(FlaskView):
    @login_required
    def index(self):
        return jsonify(body_size=[bs.serialize for bs in BodySize.query.order_by(desc(BodySize.date)).limit(10).all()])

    @login_required
    def get(self, id):
        body_size = BodySize.query.get(int(id))
        return jsonify(body_size=body_size.serialize)

    @login_required
    def patch(self, id):
        form = BodySizeForm(data=request.get_json())
        if form.validate():
            year, month, day = form.date.data.split('-')
            BodySize.query.filter_by(id=int(id)).update({
                'date': date(int(year), int(month), int(day)),
                'hip': form.hip.data,
                'waist': form.waist.data,
                'chest': form.chest.data,
                'arm': form.arm.data,
                'weight': form.weight.data
            })
            db.session.commit()
            return '', 200
        else:
            response = jsonify(error='Не верно введенеы данные. Попробуйте снова.')
            response.status_code = 409
            return response

    @login_required
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
        else:
            response = jsonify(error='Не верно введенеы данные. Попробуйте снова.')
            response.status_code = 409
            return response

    @login_required
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
