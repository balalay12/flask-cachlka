from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()
app.config.from_object('config')

CsrfProtect(app)
db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

from app import views, models


views.AccountView.register(app)
views.ProfileView.register(app)
# api.add_resource(views.Registration, '/api/reg')
# api.add_resource(views.Login, '/api/login')
# api.add_resource(views.Logout, '/api/logout')
# api.add_resource(views.CheckAuth, '/api/check_auth')
# api.add_resource(views.CheckUnique, '/api/check_unique')
