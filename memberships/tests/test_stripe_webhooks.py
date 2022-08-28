from django.urls import reverse
from django.contrib.auth.models import User, Permission

from .utils import StripeTestCase
from memberships.models import Member, Membership, FailedPayment, Payment

from datetime import datetime
from django.utils.timezone import make_aware
from funky_time import epoch_to_datetime, years_from
from web.settings import TEST_USER_PASSWORD


class CheckoutCompletedWebhookTestCase(StripeTestCase):
    def setUp(self):
        self.setup_stripe_mocks()
        self.member = Member.create(
            full_name="test person",
            preferred_name="test",
            email="test@example.com",
            password=TEST_USER_PASSWORD,
            birth_date="1991-01-01",
        )
        self.membership = Membership.objects.create(
            member=self.member, stripe_subscription_id=self.member.email
        )

    def tearDown(self):
        self.tear_down_stripe_mocks()

    def test_a_stripe_membership_subscription_is_created_for_the_member(self):
        response = self.client.post(
            reverse("stripe_webhook"),
            {
                "type": "checkout.session.completed",
                "data": {
                    "object": {
                        "setup_intent": "example_setup_intent",
                        "success_url": "https://example.com/success?donation=10",
                    }
                },
            },
            content_type="application/json",
        )

        self.assertEqual(200, response.status_code)
        self.create_subscription.assert_called()

    def test_membership_subscriptions_can_include_donations(self):
        response = self.client.post(
            reverse("stripe_webhook"),
            {
                "type": "checkout.session.completed",
                "data": {
                    "object": {
                        "setup_intent": "example_setup_intent",
                        "success_url": "https://example.com/success?donation=10",
                    }
                },
            },
            content_type="application/json",
        )
        _, kwargs = self.create_subscription.call_args

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, kwargs["donation"])

    def test_a_membership_is_created_for_the_member_in_the_database(self):
        response = self.client.post(
            reverse("stripe_webhook"),
            {
                "type": "checkout.session.completed",
                "data": {
                    "object": {
                        "setup_intent": "example_setup_intent",
                        "success_url": "https://example.com/success?donation=10",
                    }
                },
            },
            content_type="application/json",
        )
        memberships = Membership.objects.filter(member=self.member)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, memberships.count())

    def test_a_failed_payment_for_membership_gets_logged_to_db(self):
        self.member.stripe_customer_id = "cus_12345"
        self.member.save()
        response = self.client.post(
            reverse("stripe_webhook"),
            {
                "type": "invoice.payment_failed",
                "data": {
                    "object": {
                        "customer": "cus_12345",
                        "customer_email": "test@example.com",
                        "subscription": "sub_12345",
                    }
                },
            },
            content_type="application/json",
        )
        f_payments = FailedPayment.objects.all()

        self.assertEqual(1, f_payments.count())

    def test_a_successful_payment_for_membership_gets_logged_in_db(self):
        response = self.client.post(
            reverse("stripe_webhook"),
            {
                "type": "invoice.paid",
                "data": {
                    "object": {
                        "customer_email": "test@example.com",
                        "subscription": "sub_12345",
                    }
                },
                "created": 1611620481,
            },
            content_type="application/json",
        )
        payments = Payment.objects.all()

        self.assertEqual(1, payments.count())

    def test_new_member_is_given_a_membership_renewal_date_upon_payment(self):
        response = self.client.post(
            reverse("stripe_webhook"),
            {
                "type": "invoice.paid",
                "data": {
                    "object": {
                        "customer_email": "test@example.com",
                        "subscription": "sub_12345",
                    }
                },
                "created": 1611620481,
            },
            content_type="application/json",
        )
        member = Member.objects.get(id=self.member.id)

        self.assertEqual(datetime, type(member.renewal_date))

    def test_existing_membership_renewal_date_updated_upon_payment(self):
        original = datetime(2020, 1, 1, 12, 55, 59, 123456)
        self.member.renewal_date = make_aware(original)
        self.member.save()
        response = self.client.post(
            reverse("stripe_webhook"),
            {
                "type": "invoice.paid",
                "data": {
                    "object": {
                        "customer_email": "test@example.com",
                        "subscription": "sub_12345",
                    }
                },
                "created": 1611620481,
            },
            content_type="application/json",
        )
        new_datetime = years_from(1, original)
        member = Member.objects.get(id=self.member.id)

        self.assertEqual(datetime, type(member.renewal_date))
        self.assertEqual(new_datetime, member.renewal_date)

    def test_new_member_is_given_user_permission_on_payment(self):
        response = self.client.post(
            reverse("stripe_webhook"),
            {
                "type": "invoice.paid",
                "data": {
                    "object": {
                        "customer_email": "test@example.com",
                        "subscription": "sub_12345",
                    }
                },
                "created": 1611620481,
            },
            content_type="application/json",
        )
        user = User.objects.get(id=self.member.user_id)

        self.assertEqual(True, user.has_perm("memberships.has_membership"))
