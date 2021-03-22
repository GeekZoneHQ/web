from datetime import datetime, timedelta
from django import forms
from .models import Member
from django.forms import ModelForm, DateField
from django.contrib.auth import password_validation
from .models import Member


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
        from funky_time import is_younger_than, is_older_than, date_to_datetime

        birth_date = date_to_datetime(self.cleaned_data.get("birth_date"))

        if is_younger_than(0, birth_date):
            raise forms.ValidationError(
                "Unless you are a Time Lord, please enter a date in the past."
            )

        elif is_younger_than(18, birth_date):
            raise forms.ValidationError(
                "Thanks for your interest in joining Geek.Zone! We're pumped that you"
                " want to become an official epic Geek, however, as you are under 18 we"
                " need to speak to your parent or guardian. Please ask them to email"
                " trustees@geek.zone to request membership on your behalf. Thanks!"
            )

        elif is_older_than(130, birth_date):
            raise forms.ValidationError(
                "Nobody has ever lived that long! Please check your birthdate."
            )

        # FIXME JDG in the future, messages and limits like these should be admin user configurable

        return birth_date

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_validation.validate_password(password, None)

        return self.cleaned_data["password"]

    def clean_email(self):
        if Member.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("You've already registered! Please login")
        return self.cleaned_data["email"]


class MemberSettingsForm(ModelForm):
    class Meta:
        model = Member
        fields = "__all__"
        exclude = [
            "stripe_customer_id",
            "email",
            "user",
            "constitution_agreed",
            "renewal_date",
        ]  # JDG Should also exclude renewal date once we have it
        widgets = {"birth_date": DateInput()}


class MemberDetailsForm(ModelForm):
    class Meta:
        model = Member
        fields = "__all__"
        exclude = [
            "stripe_customer_id",
            "email",
            "user",
            "constitution_agreed",
            "profile_image",
        ]
