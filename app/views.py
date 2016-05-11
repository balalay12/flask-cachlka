from flask import render_template, jsonify
from flask_classy import FlaskView, request, route
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, BodySizeForm
from app.models import User, BodySize
from functools import wraps


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


class ProfileView(FlaskView):
    @login_required
    def index(self):
        user = dict()
        user['username'] = current_user.username
        user['email'] = current_user.email
        return jsonify(user)

    @login_required
    def change_password(self):
        pass


class BodysizeView(FlaskView):
    @login_required
    def index(self):
        return jsonify(body_size=[bs.serialize for bs in BodySize.query.all()])

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
            print('form not valid')
            # TODO: return errors
            return '', 200
