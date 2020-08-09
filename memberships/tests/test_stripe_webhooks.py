from django.urls import reverse

from .utils import StripeTestCase
from memberships.models import Member, Membership


class CheckoutCompletedWebhookTestCase(StripeTestCase):
    def setUp(self):
        self.setup_stripe_mocks()
        self.member = Member.create(
            full_name="test person",
            preferred_name="test",
            email="test@example.com",
            password="test",
            birth_date="1991-01-01",
        )

    def tearDown(self):
        self.tear_down_stripe_mocks()

    def test_a_stripe_sand_subscription_is_created_for_the_member(self):
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

    def test_sand_subscriptions_can_include_donations(self):
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
        self.assertEqual(1, memberships.count())
