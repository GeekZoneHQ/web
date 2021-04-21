from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

import urllib.request
import json
import stripe
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta

from .payments import handle_stripe_payment, check_member_paying
from .forms import *
from .models import Member, Membership
from .services import StripeGateway
from .tasks import task_payment_check


def validate_recaptcha(response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    secret = settings.RECAPTCHA_SECRET_KEY
    payload = {"secret": secret, "response": response}
    data = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(request)
    result = json.loads(response.read().decode())
    success = result.get("success")

    if (not result.get("success")) or (float(result.get("score")) < 0.5):
        return "fail"

    return result


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse("memberships_details"))

    if not request.method == "POST":
        return render(
            request,
            "memberships/register.html",
            {
                "form": RegistrationForm(),
                "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
            },
        )
    form = RegistrationForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "memberships/register.html",
            {
                "form": form,
                "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
            },
        )
    if not form.cleaned_data["preferred_name"]:
        form.cleaned_data["preferred_name"] = form.cleaned_data["full_name"]

    if settings.RECAPTCHA_SECRET_KEY and settings.RECAPTCHA_SITE_KEY:
        recaptchaV3_response = request.POST.get("recaptchaV3-response")
        success = validate_recaptcha(recaptchaV3_response)
        if success == "fail":
            return HttpResponse(
                "Invalid reCAPTCHA response. Please try again.", status=403
            )

    member = Member.create(
        full_name=form.cleaned_data["full_name"],
        preferred_name=form.cleaned_data["preferred_name"],
        email=form.cleaned_data["email"],
        password=form.cleaned_data["password"],
        birth_date=form.cleaned_data["birth_date"],
    )

    exec_time = datetime.utcnow() + timedelta(hours=24)
    task_payment_check.apply_async(args=(member.id,), eta=exec_time)

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
        "{}?donation={}".format(reverse("memberships_settings"), donation)
        if donation
        else reverse("memberships_settings")
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
            "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        },
    )


def thanks(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("register"))
    return HttpResponse("Registration successful.")


@csrf_exempt
def stripe_webhook(request):
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(request.body), settings.STRIPE_SECRET_KEY
        )
        return handle_stripe_payment(event)
    except ValueError as e:
        return HttpResponse("Failed to parse stripe payload", status=400)


@login_required()
def details_view(request):
    if not check_member_paying(request.user):
        return HttpResponseRedirect(reverse("confirm"))

    return render(
        request,
        "memberships/member_details.html",
        {
            "form": MemberDetailsForm(instance=request.user.member),
            "profile_image": request.user.member.profile_image,
        },
    )


@login_required()
def settings_view(request):
    if not check_member_paying(request.user):
        return HttpResponseRedirect(reverse("confirm"))

    if not request.method == "POST":
        return render(
            request,
            "memberships/member_settings.html",
            {"form": MemberSettingsForm(instance=request.user.member)},
        )

    form = MemberSettingsForm(request.POST, instance=request.user.member)
    if not form.is_valid():
        return render(request, "memberships/member_settings.html", form)

    form.save()
    return redirect(reverse("memberships_details"))
