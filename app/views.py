from flask import render_template, jsonify
from flask import request, abort
from flask_restful import Resource
from app import app, db, bcrypt
from app.forms import RegistrationForm
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
