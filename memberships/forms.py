from datetime import datetime, timedelta
from django import forms
from .models import Member
from django.contrib.auth import password_validation


class DateInput(forms.DateInput):
    input_type = "date"


class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True)
    preferred_name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    birth_date = forms.DateField(required=True, widget=DateInput)
    constitution_agreed = forms.BooleanField(required=True)
    donation = forms.DecimalField(min_value=0, decimal_places=2, required=False)

    def clean_birth_date(self, *args, **kwargs):
        from funky_time import is_18, date_to_datetime

        birth_date = date_to_datetime(self.cleaned_data.get("birth_date"))

        if is_18(birth_date) is False:
            raise forms.ValidationError(
                "Thanks for your interest in joining Geek.Zone! We're pumped that you"
                " want to become an official epic Geek, however, as you are under 18 we"
                " need to speak to your parent or guardian. Please ask them to email"
                " trustees@geek.zone to request membership on your behalf. Thanks!"
            )
        # FIXME JDG in the future, we should put messages like these in the admin area for future changes

        return birth_date

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_validation.validate_password(password, None)

        return self.cleaned_data

    def clean_email(self):
        if Member.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("You've already registered! Please login")
        return self.cleaned_data["email"]
