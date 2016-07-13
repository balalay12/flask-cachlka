import json
import unittest
import os

from app import app, db, bcrypt
from app.models import User, Categories, Exercise, BodySize, Repeats, Sets
from coverage import coverage
from datetime import date
from flask_testing import TestCase


cov = coverage(branch=True, omit=['/home/danil/coding/for_venv/flaks_cachalka/*', 'tests.py'])
cov.start()

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        app.config.from_object(os.environ['APP_SETTINGS'])
        return app

    def setUp(self):
        db.create_all()
        user = User(
                username="admin",
                email="ad@min.com",
                password=bcrypt.generate_password_hash("admin")
            )
        category = Categories(
            name='Категория 1'
        )
        exercise = Exercise(
            name='Упр 1',
            category_id=1
        )
        db.session.add(user)
        db.session.add(category)
        db.session.add(exercise)
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


class AccountTest(BaseTestCase):

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


class SetsTest(BaseTestCase):

    def test_sets(self):
        """TEST: sets crud"""

        data_200 = [dict(
            date='2016-5-23',
            exercise=1,
            exercise_name='test',
            repeats=[dict(
                weight=12,
                repeats=12
            )]
        ), dict(
            date='2016-5-23',
            exercise=1,
            exercise_name='test',
            repeats=[dict(
                weight=12,
                repeats=12
            )])]

        data_400 = [dict(
            date='',
            exercise=1,
            exercise_name='test',
            repeats=[dict(
                weight=12,
                repeats=12
            )]
        )]

        # POST
        response = self.client.post('/sets/', data=json.dumps(data_200))
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.post('/sets/', data=json.dumps(data_200))
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/sets/', data=json.dumps(data_400))
        self.assert404(response)

        set1 = Sets(
            date=date.today(),
            exercise_id=1,
            user_id=1
        )
        set2 = Sets(
            date=date.today(),
            exercise_id=1,
            user_id=2
        )
        db.session.add(set1)
        db.session.add(set2)
        db.session.commit()

        # GET all sets for current month
        response = self.client.get('/sets/')
        self.assert200(response)
        self.assertEqual(len(response.json['sets']), 1)

        # GET by id
        response = self.client.get('/sets/3')
        self.assert200(response)
        response = self.client.get('/sets/4')
        self.assert404(response)

        # PATCH
        patch_ok = dict(
            exercise=2
        )
        patch_error = dict(
            exercise=''
        )
        response = self.client.patch('/sets/3', data=json.dumps(patch_error))
        self.assert404(response)
        response = self.client.patch('/sets/4', data=json.dumps(patch_ok))
        self.assert404(response)
        response = self.client.patch('/sets/3', data=json.dumps(patch_ok))
        self.assert200(response)

        # DELETE
        response = self.client.delete('/sets/4')
        self.assert404(response)
        response = self.client.delete('/sets/3')
        self.assert200(response)

    def test_sets_for_month(self):
        """TEST: get sets for 1 month"""

        set1 = Sets(
            date=date(year=int(2016), month=int(5), day=int(4)),
            exercise_id=1,
            user_id=1
        )
        set2 = Sets(
            date=date(year=int(2016), month=int(5), day=int(7)),
            exercise_id=1,
            user_id=1
        )
        db.session.add(set1)
        db.session.add(set2)
        db.session.commit()

        response = self.client.get('/sets/5/2015')
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.get('/sets/5/2015')
        self.assert200(response)
        self.assertEqual(len(response.json['sets']), 0)
        response = self.client.get('/sets/5/2016')
        self.assert200(response)
        self.assertEqual(len(response.json['sets']), 2)

    def test_set_by_date(self):
        """TEST: get set by date"""

        set1 = Sets(
            date=date(year=int(2016), month=int(5), day=int(4)),
            exercise_id=1,
            user_id=1
        )
        set2 = Sets(
            date=date(year=int(2016), month=int(5), day=int(3)),
            exercise_id=1,
            user_id=2
        )
        db.session.add(set1)
        db.session.add(set2)
        db.session.commit()

        response = self.client.get('/sets/by_date/2016-05-3')
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.get('/sets/by_date/2016-05-3')
        self.assert200(response)
        self.assertEqual(len(response.json['day']), 0)
        response = self.client.get('/sets/by_date/2016-05-4')
        self.assert200(response)
        self.assertEqual(len(response.json['day']), 1)

class RepeatsTest(BaseTestCase):

    def test_repeats(self):
        """TEST: repeats crud"""

        data_201 = dict(
            set=1,
            weight=12.5,
            repeats=8,
        )

        data_201_patch = dict(
            set=1,
            weight=13.5,
            repeats=10,
        )

        data_400 = dict(
            set='',
            weight=12.5,
            repeats=8,
        )

        response = self.client.post('/repeats/', data=json.dumps(data_201))
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.post('/repeats/', data=json.dumps(data_400))
        self.assertEqual(response.status_code, 409)
        response = self.client.post('/repeats/', data=json.dumps(data_201))
        self.assertEqual(response.status_code, 201)

        s1 = Sets(
            date=date.today(),
            exercise_id=1,
            user_id=1
        )

        s2 = Sets(
            date=date.today(),
            exercise_id=1,
            user_id=2
        )

        r = Repeats(
            set_id=2,
            weight=12,
            repeat=43,
        )
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(r)
        db.session.commit()

        response = self.client.get('/repeats/1')
        self.assert200(response)
        response = self.client.get('/repeats/2')
        self.assert404(response)

        response = self.client.patch('/repeats/2', data=json.dumps(data_400))
        self.assert404(response)
        response = self.client.patch('/repeats/1', data=json.dumps(data_400))
        self.assertEqual(response.status_code, 409)
        response = self.client.patch('/repeats/1', data=json.dumps(data_201_patch))
        self.assert200(response)

        response = self.client.delete('/repeats/2')
        self.assert404(response)
        response = self.client.delete('/repeats/1')
        self.assert200(response)


class CategoriesTest(BaseTestCase):

    def test_categories(self):
        """TEST: get all categories"""

        response = self.client.get('/categories/')
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.get('/categories/')
        self.assert200(response)
        self.assertEqual(len(response.json), 1)


class ExerciseTest(BaseTestCase):

    def test_exercise(self):
        """TEST: exercise by category id"""

        response = self.client.get('/exercises/exercises_by_category/1')
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.get('/exercises/exercises_by_category/1')
        self.assert200(response)
        self.assertEqual(len(response.json), 1)


class ProfileTest(BaseTestCase):

    def test_profile_page(self):
        """TEST: profile page"""

        response = self.client.get('/profile/')
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.get('/profile/')
        self.assertEqual(response.json, dict(email="ad@min.com", id=1, username="admin"))


class BodysizeTest(BaseTestCase):

    def test_body_size(self):
        """TEST: crud body size"""

        data_201 = dict(
            date='2016-6-22',
            chest=12,
            waist=13,
            hip=14,
            arm=15,
            weight=16
        )

        data_200_patch = dict(
            date='2016-6-22',
            chest=56,
            waist=13,
            hip=14,
            arm=15,
            weight=16
        )

        data_409 = dict(
            chest=12,
            waist=13,
            hip=14,
            arm=15,
            weight=16
        )

        response = self.client.post('/bodysize/', data=json.dumps(data_201))
        self.assert401(response)
        self.login(**self.login_user)
        response = self.client.post('/bodysize/', data=json.dumps(data_409))
        self.assertEqual(response.status_code, 409)
        response = self.client.post('/bodysize/', data=json.dumps(data_201))
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/bodysize/')
        self.assert200(response)
        self.assertEqual(len(response.json), 1)

        body_size = BodySize(
            date=date.today(),
            chest=13,
            user_id=2
        )

        db.session.add(body_size)
        db.session.commit()
        response = self.client.get('/bodysize/2')
        self.assert404(response)
        response = self.client.get('/bodysize/1')
        self.assert200(response)
        self.assertEqual(len(response.json), 1)
        response = self.client.patch('/bodysize/2', data=json.dumps(data_200_patch))
        self.assert404(response)
        response = self.client.patch('/bodysize/1', data=json.dumps(data_409))
        self.assertEqual(response.status_code, 409)
        response = self.client.patch('/bodysize/1', data=json.dumps(data_200_patch))
        self.assert200(response)
        response = self.client.delete('/bodysize/2')
        self.assert404(response)
        response = self.client.delete('/bodysize/1')
        self.assert200(response)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print('\nCoverage report:\n')
    cov.report()
