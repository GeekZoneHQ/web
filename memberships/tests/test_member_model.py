from memberships.models import Member
from .utils import StripeTestCase
from web.settings import TEST_USER_PASSWORD


class MemberModelTestCase(StripeTestCase):
    def setUp(self):
        self.setup_stripe_mocks()

    def tearDown(self):
        self.tear_down_stripe_mocks()

    def test_a_member_gets_a_django_auth_account(self):
        member = Member.create(
            full_name="test person",
            preferred_name="test",
            email="test@example.com",
            password=TEST_USER_PASSWORD,
            birth_date="1991-01-01",
        )
        self.assertIsNotNone(member.user)
        self.assertEqual(member.email, member.user.username)

    def test_preferred_name_defaults_to_full_name(self):
        member = Member.create(
            full_name="test person",
            email="test@example.com",
            password=TEST_USER_PASSWORD,
            birth_date="1991-01-01",
        )
        self.assertEquals(member.full_name, member.preferred_name)

    def test_preferred_name_can_be_specified(self):
        member = Member.create(
            full_name="test person",
            preferred_name="test",
            email="test@example.com",
            password=TEST_USER_PASSWORD,
            birth_date="1991-01-01",
        )
        self.assertEqual("test", member.preferred_name)

    def test_a_member_is_created_as_a_stripe_customer(self):
        member = Member.create(
            full_name="test person",
            preferred_name="test",
            email="test@example.com",
            password=TEST_USER_PASSWORD,
            birth_date="1991-01-01",
        )
        self.assertEquals("example_stripe_customer", member.stripe_customer_id)
