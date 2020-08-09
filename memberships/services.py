from django.conf import settings
import stripe


class StripeGateway:
    def __init__(self, sand_price_id=None, test=False):
        stripe.api_key = settings.STRIPE_SECRET_KEY if not test else None
        self.sand_price_id = (
            "price_1HDveaJh8KDe9GPFiya9gKoZ" if not sand_price_id else sand_price_id
        )

    def upload_member(self, email):
        customer = stripe.Customer.create(email=email)
        return customer.id

    def create_checkout_session(self, member, success_url, cancel_url):
        session = stripe.checkout.Session.create(
            payment_method_types=["bacs_debit"],
            mode="setup",
            customer=member.stripe_customer_id,
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.id

    def create_subscription(self, setup_intent):
        intent = stripe.SetupIntent.retrieve(setup_intent)
        customer = stripe.Customer.retrieve(intent.customer)
        subscription = stripe.Subscription.create(
            customer=intent.customer,
            default_payment_method=intent.payment_method,
            items=[{"price": self.sand_price_id}],
        )
        return {"id": subscription.id, "email": customer.email}
