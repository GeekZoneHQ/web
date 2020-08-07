from django.test import TransactionTestCase, TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from unittest import mock
import stripe
import json

from .forms import RegistrationForm
from .models import Member, Membership


class StripeId:
    def __init__(self, id):
        self.id = id


class RegisterFormTestCase(TransactionTestCase):
    def test_signed_in_users_cannot_register(self):
        member = Member.create(
            full_name="test person",
            preferred_name="test",
            email="test@example.com",
            password="test",
            birth_date="1991-01-01",
            constitution_agreed=True,
        )
        self.client.login(username="test@example.com", password="test")
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 403)

    def test_correct_fields_are_required(self):
        response = self.client.post(reverse("register"))
        self.assertFormError(response, "form", "full_name", "This field is required.")
        self.assertFormError(response, "form", "email", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")
        self.assertFormError(response, "form", "birth_date", "This field is required.")
        self.assertFormError(
            response, "form", "constitution_agreed", "This field is required."
        )

    def test_donation_is_required_to_be_a_number(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": "test",
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
                "donation": "example_stripe_key",
            },
        )
        self.assertFormError(response, "form", "donation", "Enter a number.")

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

    def test_member_is_logged_in_after_creation(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": "test",
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
            },
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_a_member_is_created_as_a_stripe_customer(self):
        with mock.patch("stripe.Customer.create") as create_stripe_customer:
            create_stripe_customer.return_value = StripeId("example_stripe_id")
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
            create_stripe_customer.assert_called_with(email="test@example.com")

        member = Member.objects.filter(email="test@example.com").first()
        self.assertEquals(member.stripe_customer_id, "example_stripe_id")

    def test_member_is_redirected_to_confirm_page_with_donation_when_provided(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": "test",
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
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
                "password": "test",
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
            },
        )
        self.assertRedirects(response, reverse("confirm"))


class DonationConfirmPageTestCase(TransactionTestCase):
    def setUp(self):
        member = Member.create(
            full_name="test person",
            preferred_name="test",
            email="test@example.com",
            password="test",
            birth_date="1991-01-01",
            constitution_agreed=True,
        )
        self.client.login(username="test@example.com", password="test")

    def test_page_requires_authenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("confirm"))
        self.assertRedirects(response, reverse("register"))

    def test_total_with_donation_shows_correct_amount(self):
        response = self.client.get("{}?donation={}".format(reverse("confirm"), 10))
        self.assertContains(response, "Your sand membership will cost £11 a year")
        self.assertContains(
            response,
            "This is made up of a £1 Sand membership charge and a £10 donation",
        )

    def test_total_without_donation_shows_correct_amount(self):
        response = self.client.get(reverse("confirm"))
        self.assertContains(response, "Your sand membership will cost £1 a year")
        self.assertContains(
            response, "This is made up of a £1 Sand membership charge with no donation"
        )

    def test_view_has_stripe_public_key(self):
        with mock.patch("django.conf.settings.STRIPE_PUBLIC_KEY", "example_stripe_key"):
            response = self.client.get(reverse("confirm"))
            self.assertEqual(
                response.context["stripe_public_key"], "example_stripe_key"
            )

    def test_view_has_stripe_session_id(self):
        with mock.patch("stripe.checkout.Session.create") as session_create:
            session_create.return_value = StripeId("example_session_id")
            response = self.client.get(reverse("confirm"))
            self.assertEqual(
                response.context["stripe_session_id"], "example_session_id"
            )

    def test_users_who_cancel_without_a_donation_are_redirected_to_confirm(self):
        with mock.patch("stripe.checkout.Session.create") as session_create:
            response = self.client.get(reverse("confirm"))
            _, kwargs = session_create.call_args
            self.assertEqual(
                kwargs["cancel_url"], "http://testserver{}".format(reverse("confirm"))
            )

    def test_users_who_cancel_with_a_donation_are_redirected_to_confirm_with_a_donation(
        self,
    ):
        with mock.patch("stripe.checkout.Session.create") as session_create:
            response = self.client.get("{}?donation=10".format(reverse("confirm")))
            _, kwargs = session_create.call_args
            self.assertEqual(
                kwargs["cancel_url"],
                "http://testserver{}?donation=10".format(reverse("confirm")),
            )


class ThanksPageTestCase(TestCase):
    def test_page_requires_authenticated_user(self):
        response = self.client.get(reverse("thanks"), follow=True)
        self.assertRedirects(response, reverse("register"))


class CheckoutCompletedWebhookTestCase(TransactionTestCase):
    class SetupIntent:
        payment_method = "bacs_debit"
        customer = "test customer"
        customer_email = "test@example.com"

    def setUp(self):
        self.setup_intent = self.SetupIntent()
        self.member = Member.create(
            full_name="test person",
            preferred_name="test",
            email=self.setup_intent.customer_email,
            password="test",
            birth_date="1991-01-01",
            constitution_agreed=True,
        )

    def test_a_stripe_sand_subscription_is_created_for_the_member(self):
        with mock.patch("stripe.SetupIntent.retrieve") as get_setup_intent:
            get_setup_intent.return_value = self.setup_intent
            with mock.patch("stripe.Subscription.create") as create_stripe_subscription:
                response = self.client.post(
                    reverse("stripe_webhook"),
                    {
                        "type": "checkout.session.completed",
                        "data": {"object": {"setup_intent": "example_setup_intent"}},
                    },
                    content_type="application/json",
                )
                create_stripe_subscription.assert_called()

    def test_a_membership_is_created_for_the_member_in_the_database(self):
        with mock.patch("stripe.SetupIntent.retrieve") as get_setup_intent:
            get_setup_intent.return_value = self.setup_intent
            with mock.patch("stripe.Subscription.create") as create_stripe_subscription:
                create_stripe_subscription.return_value = StripeId(
                    "stripe_subscription_id"
                )
                response = self.client.post(
                    reverse("stripe_webhook"),
                    {
                        "type": "checkout.session.completed",
                        "data": {"object": {"setup_intent": "example_setup_intent"}},
                    },
                    content_type="application/json",
                )
                memberships = Membership.objects.filter(member=self.member)
                self.assertEqual(1, memberships.count())
