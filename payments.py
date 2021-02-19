from django.contrib.auth.models import Permission, User

from .models import Member, Membership, FailedPayment, Payment
from funky_time import epoch_to_datetime


def handle_stripe_payment(event):
    if event["type"] == "invoice.payment_failed":
        f_payment = FailedPayment.objects.create(
            stripe_customer_id=event["data"]["object"]["customer"],
            stripe_subscription_id=event["data"]["object"]["subscription"],
            stripe_event_type=event["type"],
        )
        if event["type"] == "invoice.payment_succeeded":
            member = Member.objects.get(email=event["data"]["object"]["customer_email"])
            log_payment(event, member)
            update_last_payment(event, member)
            add_user_sand_permission(member)


def log_payment(event, member):
    # Log payment for a member in the database
    payment = Payment.objects.create(
        member=member,
        stripe_subscription_id=event["data"]["object"]["subscription"],
    )


def update_last_payment(event, member):
    # Store payment DateTime in membership model
    membership = Membership.objects.get(member=member)
    membership.last_payment_time = epoch_to_datetime(event["created"])
    membership.save()


def add_user_sand_permission(member):
    # Give user 'has_sand_membership' permission
    user = User.objects.get(id=member.user_id)
    perm = Permission.objects.get(codename="has_sand_membership")
    user.user_permissions.add(perm)
