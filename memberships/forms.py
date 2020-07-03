from django import forms
from .models import Member

class DateInput(forms.DateInput):
    input_type = 'date'

class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True)
    preferred_name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)
    birth_date = forms.DateField(required=True, widget=DateInput)
    constitution_agreed = forms.BooleanField(required=True)
