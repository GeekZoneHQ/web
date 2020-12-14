from django.urls import reverse
from .utils import StripeTestCase

class LoginFormTestCase(StripeTestCase):
    def setUp(self):
        self.setup_stripe_mocks()

    def tearDown(self):
        self.tear_down_stripe_mocks()

    def test_newly_registered_user_can_login(self):
        # Register a user using the form
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "test person",
                "email": "test@example.com",
                "password": "k38m1KIhIUzeA^UL",
                "birth_date": "1991-01-01",
                "constitution_agreed": "on",
            },
            follow=True
        )
        self.assertTrue(response.context["user"].is_authenticated)

        # Log them out
        response = self.client.get(reverse("memberships_logout"), follow=True)
        self.assertFalse(response.context["user"].is_authenticated)

        # Log them back in using the login form
        response = self.client.post(
            reverse("memberships_login"),
            {
                "username": "test@example.com",
                "password": "k38m1KIhIUzeA^UL"
            },
            follow=True
        )
        self.assertTrue(response.context["user"].is_authenticated)
