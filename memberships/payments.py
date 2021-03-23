from django.contrib.auth.models import Permission
from django.http import HttpResponse
from urllib.parse import parse_qs, urlparse

from memberships.models import Member, Membership, FailedPayment, Payment
from funky_time import epoch_to_datetime, years_from
from .services import StripeGateway
from datetime import datetime


def handle_stripe_payment(event):
    if event["type"] == "checkout.session.completed":
        return session_completed(event)
    if event["type"] == "invoice.payment_failed":
        FailedPayment.objects.create(
            member=Member.objects.get(
                stripe_customer_id=event["data"]["object"]["customer"]
            ),
            stripe_subscription_id=event["data"]["object"]["subscription"],
            stripe_event_type=event["type"],
        )
        return HttpResponse(200)
    if event["type"] == "invoice.payment_succeeded":
        member = Member.objects.get(email=event["data"]["object"]["customer_email"])
        log_successful_payment(event, member)
        update_last_payment(event, member)
        add_user_sand_permission(member)
        set_sand_renewal_date(member)
        return HttpResponse(200)

    return HttpResponse(200)


def session_completed(event):
    client = StripeGateway()
    try:
        donation = donation_from_url(event.data.object.success_url)
        subscription = client.create_subscription(
            event.data.object.setup_intent, donation=donation
        )
        # todo: member not found?
        # todo: unable to create membership? delete from stripe? alert someone?
        member = Member.objects.get(email=subscription["email"])
        Membership.objects.create(
            member=member, stripe_subscription_id=subscription["id"]
        )
        return HttpResponse(200)
    except Exception as e:
        # todo: should this be a 5xx?
        return HttpResponse(e, status=500)


def donation_from_url(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if "donation" in query:
        return int(query["donation"][0])
    else:
        return None


def log_successful_payment(event, member):
    # Log payment for a member in the database
    Payment.objects.create(
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
    perm = Permission.objects.get(codename="has_sand_membership")
    member.user.user_permissions.add(perm)


def set_sand_renewal_date(member):
    if member.renewal_date is None or member.renewal_date == datetime.now():
        # Renewal datetime is now or not previously set
        member.renewal_date = years_from(1, datetime.now())
    else:
        # Payment was overdue or early
        member.renewal_date = years_from(1, member.renewal_date)
    member.save()
