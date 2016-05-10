from flask import render_template, jsonify
from flask_classy import FlaskView, request, route
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User


@app.route('/')
def index():
    return render_template('main.html')


class AccountView(FlaskView):
    @route('/registration/', methods=['POST'])
    def registration(self):
        # TODO: user auth check
        form = RegistrationForm(data=request.get_json())
        if form.validate():
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=bcrypt.generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            return jsonify(ok='ok')
        else:
            return jsonify(not_ok='form not valid')

    @route('/login/', methods=['POST'])
    def login(self):
        # TODO: check auth user
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

    def check_auth(self):
        if current_user.is_authenticated:
            return '', 200
        else:
            return '', 401

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
