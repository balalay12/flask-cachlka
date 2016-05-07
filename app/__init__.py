from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from flask_restful import Api


app = Flask(__name__)
app.config.from_object('config')

CsrfProtect(app)
db = SQLAlchemy(app)
api = Api(app)

from app import views, models


api.add_resource(views.Registration, '/api/reg')
