from flask_wtf import Form
from wtforms import StringField, PasswordField, DateField, FloatField
from wtforms.validators import DataRequired, Email


class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class BodySizeForm(Form):
    date = DateField('Date', validators=[DataRequired()])
    chest = FloatField('Chest')
    waist = FloatField('Waist')
    hip = FloatField('Hip')
    arm = FloatField('Arm')
    weight = FloatField('Weight')
