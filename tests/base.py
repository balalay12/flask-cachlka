from flask_testing import TestCase
from app import app, db, bcrypt
from app.models import User


class BaseTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        user = User(
                username="admin",
                email="ad@min.com",
                password=bcrypt.generate_password_hash("admin")
            )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
