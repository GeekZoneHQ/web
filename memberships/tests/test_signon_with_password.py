from json import loads
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from memberships.views import signon_with_password
from django.contrib.auth.models import User
from .api_utils import APITestCase

class SignonWithPasswordTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.create_user('example', 'Secure123!', 'example@example.com')


    def test_valid_username_and_password_return_token(self):
        request = self.factory.post(
            '/memberships/signonWithPassword/',
            { 'email': 'example@example.com', 'password': 'Secure123!' },
            format='json'
        )
        resp = signon_with_password(request)
        data: dict = loads(resp.content.decode('utf-8'))

        token = data["token"]
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.is_token(token))
