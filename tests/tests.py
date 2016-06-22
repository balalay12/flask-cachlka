import json
import unittest

from app import app, db, bcrypt
from app.models import User
from flask_testing import TestCase


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

    login_user = {'username': 'admin', 'password': 'admin'}
    login_wrong_password = {'username': 'admin', 'password': 'admin1'}
    login_wrong_data = {'username': 'admin1', 'password': 'admin1'}
    reg_user = {'username': 'test', 'email': 'te@st.com', 'password': 'test'}
    reg_user_wrong = {'username': 'test', 'email': 'te@', 'password': 'test'}
    change_password = {'old': login_user['password'], 'new': 'new', 'confirm': 'new'}

    def login(self, username, password):
        data = dict(
            username=username,
            password=password
        )
        return self.client.post('/account/login/', data=json.dumps(data))

    def logout(self):
        return self.client.get('/account/logout/')


class LoginTest(BaseTestCase):

    def test_registrtion(self):
        """TEST: user registration"""

        # registration with bad data
        response = self.client.post('/account/registration/', data=json.dumps(self.reg_user_wrong))
        self.assert404(response)

        # registration good
        response = self.client.post('/account/registration/', data=json.dumps(self.reg_user))
        self.assertEqual(response.status_code, 201)

        # registration when user authorized
        self.login(**self.login_user)
        response = self.client.post('/account/registration/', data=json.dumps(self.reg_user))
        self.assertEqual(response.status_code, 409)

    def test_login(self):
        """TEST: user login and logout"""

        # logout unauthorized user
        response = self.logout()
        self.assert401(response)

        # login not found user
        response = self.login(**self.login_wrong_data)
        self.assert404(response)

        # login user with wrong password
        response = self.login(**self.login_wrong_password)
        self.assert404(response)

        # good login
        response = self.login(**self.login_user)
        self.assert200(response)

        # good logout
        response = self.logout()
        self.assert200(response)

    def test_check_auth(self):
        """TEST: check auth"""

        response = self.client.get('/account/check_auth/')
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.get('/account/check_auth/')
        self.assert200(response)

    def test_check_unique(self):
        """TEST: check_unique"""

        username_404 = {'username': 'admin'}
        username_200 = {'username': 'admin1'}
        email_404 = {'email': 'ad@min.com'}
        email_200 = {'email': 'ad1@min.com'}
        response = self.client.post('/account/check_unique/', data=json.dumps(username_404))
        self.assert404(response)
        response = self.client.post('/account/check_unique/', data=json.dumps(email_404))
        self.assert404(response)
        response = self.client.post('/account/check_unique/', data=json.dumps(username_200))
        self.assert200(response)
        response = self.client.post('/account/check_unique/', data=json.dumps(email_200))
        self.assert200(response)

    def test_change_password(self):
        """TEST: change password"""

        data_200 = {'old': self.login_user['password'], 'new': 'new', 'confirm': 'new'}
        data_wrong_old = {'old': 'bad_pass', 'new': 'new', 'confirm': 'new'}
        data_wrong_new = {'old': self.login_user['password'], 'new': 'new1', 'confirm': 'new'}
        data_wrong_confirm = {'old': self.login_user['password'], 'new': 'new', 'confirm': 'new1'}

        response = self.client.post('/account/change_password/', data=json.dumps(data_wrong_old))
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.post('/account/change_password/', data=json.dumps(data_wrong_old))
        self.assert404(response)
        response = self.client.post('/account/change_password/', data=json.dumps(data_wrong_new))
        self.assert404(response)
        response = self.client.post('/account/change_password/', data=json.dumps(data_wrong_confirm))
        self.assert404(response)
        response = self.client.post('/account/change_password/', data=json.dumps(data_200))
        self.assert200(response)

if __name__ == '__main__':
    unittest.main()
