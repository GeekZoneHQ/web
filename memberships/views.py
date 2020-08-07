from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import stripe

from .forms import RegistrationForm
from .models import Member

stripe.api_key = settings.STRIPE_SECRET_KEY


def register(request):
    if not request.method == "POST":
        return render(
            request, "memberships/register.html", {"form": RegistrationForm()}
        )

    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, "memberships/register.html", {"form": form})

    if not form.cleaned_data["preferred_name"]:
        form.cleaned_data["preferred_name"] = form.cleaned_data["full_name"]

    Member.create(
        full_name=form.cleaned_data["full_name"],
        preferred_name=form.cleaned_data["preferred_name"],
        email=form.cleaned_data["email"],
        password=form.cleaned_data["password"],
        birth_date=form.cleaned_data["birth_date"],
        constitution_agreed=form.cleaned_data["constitution_agreed"],
    )

    donation = request.POST.get("donation")
    if donation:
        confirmation_url = "{}?donation={}".format(reverse("confirm"), donation)
        return HttpResponseRedirect(confirmation_url)

    return HttpResponseRedirect(reverse("confirm"))


def confirm(request):
    donation = request.GET.get("donation")
    total = 1 if not donation else int(donation) + 1
    return render(
        request, "memberships/confirm.html", {"donation": donation, "total": total},
    )


def thanks(request):
    return HttpResponse("Registration successful.")
