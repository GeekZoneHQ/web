from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import authenticate, login
from urllib.parse import parse_qs, urlparse
import json
import stripe

from .forms import *
from .models import Member, Membership
from .services import StripeGateway


def register(request):
    if request.user.is_authenticated:
        return HttpResponse("cannot register while logged in", status=403)

    if not request.method == "POST":
        return render(
            request, "memberships/register.html", {"form": RegistrationForm()}
        )

    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, "memberships/register.html", {"form": form})

    if not form.cleaned_data["preferred_name"]:
        form.cleaned_data["preferred_name"] = form.cleaned_data["full_name"]

    member = Member.create(
        full_name=form.cleaned_data["full_name"],
        preferred_name=form.cleaned_data["preferred_name"],
        email=form.cleaned_data["email"],
        password=form.cleaned_data["password"],
        birth_date=form.cleaned_data["birth_date"],
    )

    login(request, member.user)

    donation = request.POST.get("donation")
    if donation:
        confirmation_url = "{}?donation={}".format(reverse("confirm"), donation)
        return HttpResponseRedirect(confirmation_url)

    return HttpResponseRedirect(reverse("confirm"))


def confirm(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("register"))

    donation = request.GET.get("donation")
    total = 1 if not donation else int(donation) + 1

    cancel_url = (
        "{}?donation={}".format(reverse("confirm"), donation)
        if donation
        else reverse("confirm")
    )
    success_url = (
        "{}?donation={}".format(reverse("thanks"), donation)
        if donation
        else reverse("thanks")
    )
    stripe_gateway = StripeGateway()
    session_id = stripe_gateway.create_checkout_session(
        member=request.user.member,
        success_url=request.build_absolute_uri(success_url),
        cancel_url=request.build_absolute_uri(cancel_url),
    )

    return render(
        request,
        "memberships/confirm.html",
        {
            "donation": donation,
            "total": total,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "stripe_session_id": session_id,
        },
    )


def thanks(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("register"))
    return HttpResponse("Registration successful.")


class StripeWebhook:
    def __init__(self):
        self.event_handlers = {"checkout.session.completed": self._session_completed}
        self.client = StripeGateway()

    def handle(self, event):
        event_handler = self.event_handlers.get(event.type, self._default_handler)
        return event_handler(event)

    # todo: fix stripe webhook returning 500
    # todo: the fix is client.create_subscription is not returning an id
    def _session_completed(self, event):
        try:
            donation = self._donation_from_url(event.data.object.success_url)
            subscription = self.client.create_subscription(
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

    def _default_handler(self, event):
        return HttpResponse(200)

    def _donation_from_url(self, url):
        parsed = urlparse(url)
        query = parse_qs(parsed.query)

        if "donation" in query:
            return int(query["donation"][0])
        else:
            return None


@csrf_exempt
def stripe_webhook(request):
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(request.body), settings.STRIPE_SECRET_KEY
        )
        stripe_webhook = StripeWebhook()
        return stripe_webhook.handle(event)
    except ValueError as e:
        return HttpResponse("Failed to parse stripe payload", status=400)


def login_view(request):
    memberloiginform = MemberLoginForm()
    context = {'form': memberloiginform}
    return render(request, 'memberships/login.html', context)

def logout_view(request):
    logout(request)
    return redirect(reverse("register"))