from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()
app.config.from_object('config')

CsrfProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

from app import views, models


views.AccountView.register(app)
views.ProfileView.register(app)
views.BodysizeView.register(app)
views.SetsView.register(app)
views.CategoriesView.register(app)
views.ExercisesView.register(app)
views.RepeatsView.register(app)
