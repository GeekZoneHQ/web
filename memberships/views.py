from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import transaction

from .forms import RegistrationForm
from .models import Member

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
    return HttpResponseRedirect(reverse("thanks"))


def thanks(request):
    return HttpResponse("Registration successful.")
