from datetime import datetime, timedelta
from django import forms
from .models import Member
from django.utils.safestring import mark_safe

class DateInput(forms.DateInput):
    input_type = "date"


class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True)
    preferred_name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        max_length=255, required=True, widget=forms.PasswordInput
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
        password = self.cleaned_data.get('password')
        if len(password) <= 16:
            raise forms.ValidationError(mark_safe('Password too short, '
                                                  'it must be <a href="https://en.wikipedia.org/wiki/Wikipedia:10,000_'
                                                  'most_common_passwords" target="_blank">'
                                                  'longer than 16 characters</a>. '
                                                  'Use <a href="http://lastpass.com" target="_blank">LastPass</a>'
                                                  ' to generate and store your passwords!'))
        return password
