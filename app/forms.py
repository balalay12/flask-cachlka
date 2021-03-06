from flask_wtf import Form
from wtforms import StringField, PasswordField, DateField, FloatField, IntegerField
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


class EditExercise(Form):
    exercise = IntegerField('Exercise', validators=[DataRequired()])


class RepeatForm(Form):
    set = IntegerField('Set', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    repeats = IntegerField('Repeats', validators=[DataRequired()])
