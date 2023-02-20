from django.urls import reverse
from django.test import TestCase, override_settings
from unittest import mock

from .utils import StripeTestCase
from memberships.models import Member, Membership
from web.settings import TEST_USER_PASSWORD, TEST_USER_PASSWORD_BAD


@override_settings(RECAPTCHA_SECRET_KEY=None, RECAPTCHA_SITE_KEY=None)
class RegisterFormTestCase(StripeTestCase):
    def setUp(self):
        self.setup_stripe_mocks()

    def tearDown(self):
        self.tear_down_stripe_mocks()

    def test_signed_in_users_cannot_register(self):
        member = Member.create(
            full_name="test person",
            preferred_name="test",
            email="test@example.com",
            password=TEST_USER_PASSWORD,
            birth_date="1991-01-01",
        )

        self.client.login(username="test@example.com", password=TEST_USER_PASSWORD)

        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 302)

    def test_correct_fields_are_required(self):
        required_string = "This field is required."
        response = self.client.post(reverse("register"))
        self.assertFormError(response, "form", "full_name", required_string)
        self.assertFormError(response, "form", "email", required_string)
        self.assertFormError(response, "form", "password", required_string)
        self.assertFormError(response, "form", "birth_date", required_string)
        self.assertFormError(response, "form", "constitution_agreed", required_string)
        self.assertFormError(response, "form", "constitutional_post", required_string)
        self.assertFormError(response, "form", "constitutional_email", required_string)

    def test_donation_is_required_to_be_a_number(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": TEST_USER_PASSWORD,
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
                "constitutional_post": "on",
                "constitutional_email": "on",
                "donation": "example_stripe_key",
            },
        )
        self.assertFormError(response, "form", "donation", "Enter a number.")

    def test_member_is_logged_in_after_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": TEST_USER_PASSWORD,
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
                "constitutional_post": "on",
                "constitutional_email": "on",
            },
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_member_is_redirected_to_confirm_page_with_donation_when_provided(
        self,
    ):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": TEST_USER_PASSWORD,
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
                "constitutional_post": "on",
                "constitutional_email": "on",
                "donation": 10,
            },
        )
        self.assertRedirects(response, "{}?donation=10".format(reverse("confirm")))

    def test_member_is_redirected_to_confirm_page_without_donation_when_not_provided(
        self,
    ):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": TEST_USER_PASSWORD,
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
                "constitutional_post": "on",
                "constitutional_email": "on",
            },
        )
        self.assertRedirects(response, reverse("confirm"))

    def test_registration_rejected_on_short_common_passwords(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": TEST_USER_PASSWORD_BAD,
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
                "constitutional_post": "on",
                "constitutional_email": "on",
            },
        )
        self.assertFormError(
            response,
            "form",
            "password",
            "This password is too short. It must contain at least 10 characters.",
        )
        self.assertFormError(
            response, "form", "password", "This password is too common."
        )

    def test_existing_member_cannot_reregister(self):
        Member.create(
            full_name="test person",
            email="test@example.com",
            password=TEST_USER_PASSWORD,
            birth_date="1991-01-01",
        )

        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": TEST_USER_PASSWORD,
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
                "constitutional_post": "on",
                "constitutional_email": "on",
            },
        )

        self.assertFormError(
            response,
            "form",
            "email",
            "You've already registered! Please login",
        )


class DonationConfirmPageTestCase(StripeTestCase):
    def setUp(self):
        self.setup_stripe_mocks()

        member = Member.create(
            full_name="test person",
            preferred_name="test",
            email="test@example.com",
            password=TEST_USER_PASSWORD,
            birth_date="1991-01-01",
        )
        self.client.force_login(member.user)

    def tearDown(self):
        self.tear_down_stripe_mocks()

    def test_page_requires_authenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("confirm"))
        self.assertRedirects(response, reverse("register"))

    def test_total_with_donation_shows_correct_amount(self):
        response = self.client.get("{}?donation={}".format(reverse("confirm"), 10.00))
        self.assertContains(response, "Your membership will cost £11.00 a year")
        self.assertContains(
            response,
            "This is made up of a £1 membership charge and a £10.00 donation",
        )

    def test_total_without_donation_shows_correct_amount(self):
        response = self.client.get(reverse("confirm"))

        self.assertContains(response, "Your membership will cost £1.00 a year")
        self.assertContains(
            response,
            "This is made up of a £1 membership charge with no donation",
        )

    @mock.patch("django.conf.settings.STRIPE_PUBLIC_KEY", "example_stripe_key")
    def test_view_has_stripe_public_key(self):
        response = self.client.get(reverse("confirm"))
        self.assertEqual(response.context["stripe_public_key"], "example_stripe_key")

    def test_view_has_stripe_session_id(self):
        response = self.client.get(reverse("confirm"))
        self.assertEqual(response.context["stripe_session_id"], "example_session_id")

    def test_users_without_a_donation_are_sent_to_the_correct_cancel_and_success_urls(
        self,
    ):
        response = self.client.get(reverse("confirm"))
        _, kwargs = self.create_checkout_session.call_args
        self.assertEqual(
            kwargs["cancel_url"],
            "http://testserver{}".format(reverse("confirm")),
        )
        self.assertEqual(
            kwargs["success_url"],
            "http://testserver{}".format(reverse("memberships_settings")),
        )

    def test_users_with_a_donation_are_sent_to_the_correct_cancel_and_success_urls(
        self,
    ):
        self.client.get("{}?donation=10.00".format(reverse("confirm")))
        _, kwargs = self.create_checkout_session.call_args
        self.assertEqual(
            kwargs["cancel_url"],
            "http://testserver{}?donation=10.00".format(reverse("confirm")),
        )
        self.assertEqual(
            kwargs["success_url"],
            "http://testserver{}?donation=10.00".format(
                reverse("memberships_settings")
            ),
        )


class ThanksPageTestCase(TestCase):
    def test_page_requires_authenticated_user(self):
        response = self.client.get(reverse("thanks"), follow=True)
        self.assertRedirects(response, reverse("register"))
