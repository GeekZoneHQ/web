from json import loads
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from .utils import APITestCase, is_token


class SignonWithPasswordTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.create_member('example', 'Secure123!', 'example@example.com')

    def test_valid_username_and_password_return_token(self):
        resp = self.client.post(
            reverse('signonWithPassword'),
            {'email': 'example@example.com', 'password': 'Secure123!'},
            format='json'
        )
        data: dict = loads(resp.content.decode('utf-8'))

        token = data["token"]
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(is_token(token), f"Token format not valid: {token}")

    def test_missing_email_returns_bad_request(self):
        resp = self.client.post(
            reverse('signonWithPassword'),
            {'password': 'Secure123!'},
            format='json'
        )
        data: dict = loads(resp.content.decode('utf-8'))

        # token = data["token"]
        self.assertEqual(resp.status_code, 400)
        # self.assertTrue(is_token(token), f"Token format not valid: {token}")
