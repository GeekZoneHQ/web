from collections import namedtuple
from django.test import TestCase
from unittest import mock

from memberships.services import StripeGateway

Member = namedtuple("Member", "stripe_customer_id")
SetupIntent = namedtuple("SetupIntent", "customer payment_method")
Customer = namedtuple("Customer", "id email")
Session = namedtuple("Session", "id")
Subscription = namedtuple("Subscription", "id")
Price = namedtuple("Price", "id")


class StripeGatewayTestCase(TestCase):
    @mock.patch("stripe.Customer.create", autospec=True)
    def test_upload_member_creates_a_stripe_customer_record(self, create_customer):
        create_customer.return_value = Customer(
            "example_customer_id", "test@example.com"
        )

        stripe_gateway = StripeGateway()
        customer_id = stripe_gateway.upload_member(email="test@example.com")

        create_customer.assert_called_with(email="test@example.com")
        self.assertEquals("example_customer_id", customer_id)

    @mock.patch("stripe.checkout.Session.create", autospec=True)
    def test_create_checkout_session_creates_a_stripe_bacs_session(
        self, create_session
    ):
        create_session.return_value = Session("example_session_id")

        stripe_gateway = StripeGateway()
        session_id = stripe_gateway.create_checkout_session(
            Member("example_customer_id"), "success-url", "cancel-url"
        )

        create_session.assert_called_with(
            payment_method_types=["bacs_debit"],
            mode="setup",
            customer="example_customer_id",
            success_url="success-url",
            cancel_url="cancel-url",
        )
        self.assertEquals("example_session_id", session_id)

    @mock.patch("stripe.Customer.retrieve", autospec=True)
    @mock.patch("stripe.SetupIntent.retrieve", autospec=True)
    @mock.patch("stripe.Subscription.create", autospec=True)
    def test_create_subscription_creates_a_membership_in_stripe(
        self, create_subscription, get_intent, get_customer
    ):
        get_intent.return_value = SetupIntent("example_customer", "a_payment_method")
        get_customer.return_value = Customer("customer_id", "test@example.com")
        create_subscription.return_value = Subscription("stripe_subscription_id")

        stripe_gateway = StripeGateway("example_membership_price")
        result = stripe_gateway.create_subscription("example_setup_intent_id")

        create_subscription.assert_called_with(
            customer="example_customer",
            default_payment_method="a_payment_method",
            items=[{"price": stripe_gateway.membership_price_id}],
        )
        self.assertEquals(
            {"id": "stripe_subscription_id", "email": "test@example.com"},
            result,
        )

    @mock.patch("stripe.Price.create", autospec=True)
    @mock.patch("stripe.Customer.retrieve", autospec=True)
    @mock.patch("stripe.SetupIntent.retrieve", autospec=True)
    @mock.patch("stripe.Subscription.create", autospec=True)
    def test_create_subscription_with_a_donation_includes_a_donation_price(
        self, create_subscription, get_intent, get_customer, create_price
    ):
        get_intent.return_value = SetupIntent("example_customer", "a_payment_method")
        get_customer.return_value = Customer("customer_id", "test@example.com")
        create_subscription.return_value = Subscription("stripe_subscription_id")
        create_price.return_value = Price("donation_price_id")

        stripe_gateway = StripeGateway(
            membership_price_id="membership_price_id",
            donation_product_id="donation_product_id",
        )
        result = stripe_gateway.create_subscription(
            "example_setup_intent_id", donation=10
        )

        create_price.assert_called_with(
            unit_amount=10 * 100,
            currency="gbp",
            recurring={"interval": "year"},
            product=stripe_gateway.donation_product_id,
        )
        _, kwargs = create_subscription.call_args
        self.assertIn({"price": "donation_price_id"}, kwargs["items"])
