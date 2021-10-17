from django.conf import settings
import stripe


class StripeGateway:
    def __init__(self, sand_price_id=None, donation_product_id=None, test=False):
        stripe.api_key = settings.STRIPE_SECRET_KEY if not test else None
        self.sand_price_id = (
            sand_price_id if not settings.SAND_PRICE_ID else settings.SAND_PRICE_ID
        )
        self.donation_product_id = (
            donation_product_id
            if not settings.DONATION_PRODUCT_ID
            else settings.DONATION_PRODUCT_ID
        )

    def upload_member(self, email):
        customer = stripe.Customer.create(email=email)
        return customer.id

    def create_checkout_session(self, member, success_url, cancel_url, donation):
        session = stripe.checkout.Session.create(
            payment_method_types=["bacs_debit"],
            mode="setup",
            customer=member.stripe_customer_id,
            success_url=success_url,
            cancel_url=cancel_url,
            # line_items=[{
            #     'amount': donation,
            #     'currency': 'gbp',
            #     'quantity': 1,
            #     'name': 'Donation',
            # }]
        )
        return session.id

    def create_subscription(self, setup_intent, donation=None):
        intent = stripe.SetupIntent.retrieve(setup_intent)
        customer = stripe.Customer.retrieve(intent.customer)

        items = [{"price": self.sand_price_id}]
        if donation:
            price = stripe.Price.create(
                unit_amount_decimal=donation,
                currency="gbp",
                recurring={"interval": "year"},
                product=self.donation_product_id,
            )
            items.append({"price": price.id})

        subscription = stripe.Subscription.create(
            customer=intent.customer,
            default_payment_method=intent.payment_method,
            items=items,
        )
        return {"id": subscription.id, "email": customer.email}
