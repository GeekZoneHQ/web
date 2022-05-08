from django.test import TransactionTestCase
from unittest import mock


class StripeTestCase(TransactionTestCase):
    def setup_stripe_mocks(self):
        self._upload_member()
        self._create_subscription()
        self._create_checkout_session()

    def tear_down_stripe_mocks(self):
        self.upload_member_patcher.stop()
        self.create_subscription_patcher.stop()
        self.create_checkout_session_patcher.stop()

    def patch(self, function):
        return mock.patch(
            f"memberships.services.StripeGateway.{function}", autospec=True
        )

    def _upload_member(self):
        self.upload_member_patcher = self.patch("upload_member")
        self.upload_member = self.upload_member_patcher.start()
        self.upload_member.return_value = "example_stripe_customer"

    def _create_subscription(self):
        self.create_subscription_patcher = self.patch("create_subscription")
        self.create_subscription = self.create_subscription_patcher.start()
        self.create_subscription.return_value = {
            "email": "test@example.com",
            "id": "stripe_subscription_id",
        }

    def _create_checkout_session(self):
        self.create_checkout_session_patcher = self.patch("create_checkout_session")
        self.create_checkout_session = self.create_checkout_session_patcher.start()
        self.create_checkout_session.return_value = "example_session_id"
