class StripeGateway:
    # def __init__(self):
    #     stripe.api_key = settings.STRIPE_SECRET_KEY
    #     self.sand_price_id = "price_1H1ekvJh8KDe9GPF5hhB57QK"

    def upload_member(self, email):
        pass

    def create_checkout_session(self, member, success_url, cancel_url):
        pass

    def create_subscription(self, setup_intent):
        pass
        # intent = stripe.SetupIntent.retrieve(setup_intent)
        # customer = stripe.Customer.retrieve(intent.customer)
        # subscription = stripe.Subscription.create(
        #     customer=intent.customer,
        #     default_payment_method=intent.payment_method,
        #     items=[{"price": self.sand_price_id}],
        # )

        # return {"email": customer.email}
        # # return self.SubscriptionResponse(intent, customer, subscription)
