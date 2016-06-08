import unittest

from base import BaseTestCase


class Tests(BaseTestCase):

    # def test_index_page(self):
    #     """TEST: render index page"""
    #
    #     response = self.client.get('/', content_type='html/text')
    #     self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        """TEST: user registration"""

        response = self.client.post('/account/registration/', data=dict(username="test", email="te@st.com", password="test"))
        self.assertEqual(response.status_code, 201)

    def test_registration_validation(self):
        """TEST: registration validation"""

        response = self.client.post('/account/registration/', data=dict(username="test", email="te@", password="test"))
        self.assertEqual(response.status_code, 404)

    def test_user_login(self):
        """TEST: user login"""

        response = self.client.post('/account/login/', data=dict(username="admin", password="admin"))
        self.assertEqual(response.status_code, 200)

    def test_login_undefined_user(self):
        """TEST: username not found in database"""

        response = self.client.post('/account/login/', data=dict(username="test", password="test"))
        self.assertEqual(response.status_code, 404)

    def test_login_wrong_password(self):
        """TEST: password is wrong"""

        response = self.client.post('/account/login/', data=dict(username="admin", password="test"))
        self.assertEqual(response.status_code, 404)

    # def test_unique(self):
    #     """TEST: unique username or email"""
    #
    #     response_username = self.client.post('/account/check_unique/', data=dict(email="admin"))
    #     self.assertEqual(response_username.status_code, 404)

    # def test_password_change(self):
    #     """TEST: change password"""
    #
    #     login = self.client.post('/account/login/', data=dict(username="admin", password="admin"))
    #     response = self.client.post('/account/change_password/', data=dict(old='admin', new='newadmin', confirm='newadmin'))
    #     print(response.data)
    #     self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()