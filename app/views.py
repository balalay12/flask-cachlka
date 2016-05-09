from flask import render_template, jsonify, session
from flask import request
from flask_restful import Resource
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User


@app.route('/')
def index():
    return render_template('main.html')


class Registration(Resource):
    def post(self):
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
            print(form.errors)
            return jsonify(not_ok='form not valid')


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(
                user.password,
                data['password']):
            session['logged_in'] = True
            session['username'] = user.username
            status = True
        else:
            status = False
        return jsonify({'result': status})


class Logout(Resource):
    def post(self):
        session.pop('logged_in')
        session.pop('username')
        print('user logout')
        return '', 200


class CheckAuth(Resource):
    def post(self):
        if 'logged_in' in session:
            return '', 200
        else:
            return '', 401


class CheckUnique(Resource):
    def post(self):
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
