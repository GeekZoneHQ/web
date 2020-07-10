from django.test import TransactionTestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .forms import RegistrationForm
from .models import Member


class RegisterFormTestCase(TransactionTestCase):
    def test_correct_fields_are_required(self):
        response = self.client.post(reverse("register"))
        self.assertFormError(response, "form", "full_name", "This field is required.")
        self.assertFormError(response, "form", "email", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")
        self.assertFormError(response, "form", "birth_date", "This field is required.")
        self.assertFormError(
            response, "form", "constitution_agreed", "This field is required."
        )

    def test_preferred_name_defaults_to_full_name(self):
        self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": "test",
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
            },
        )
        member = Member.objects.get(email="test@example.com")
        self.assertEqual(member.preferred_name, "test person")

    def test_preferred_name_can_be_specified(self):
        self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "preferred_name": "i prefer this",
                "email": "test@example.com",
                "password": "test",
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
            },
        )
        member = Member.objects.get(email="test@example.com")
        self.assertEqual(member.preferred_name, "i prefer this")

    def test_a_member_gets_a_django_auth_account(self):
        self.assertEqual(0, User.objects.count())
        self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": "test",
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
            },
        )
        user = User.objects.filter(username="test@example.com")
        self.assertEqual(1, user.count())
