import re
from django.test import TestCase
from django.contrib.auth.models import User
from memberships.models import Member, Membership

class APITestCase(TestCase):

    JWT_REGEX = r"/^([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_\-\+\/=]*)/gm"

    def create_user(self, name, password, email) -> None:
        self.member = Member.create(
            full_name="test person",
            preferred_name=name,
            email=email,
            password=password,
            birth_date="1991-01-01",
        )
    
    def is_token(string: str) -> bool:
        if re.match(APITestCase.JWT_REGEX, string):
            return True
        return False
