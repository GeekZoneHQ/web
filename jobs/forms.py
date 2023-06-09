from django import forms
from django.core.exceptions import ValidationError

from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'sector', 'contract_type', 'pay', 'employer_name',
                  'incorporation_number', 'website', 'expiry_date', 'application_url']

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')

        # Check if the expiry_date is in a valid format
        if not expiry_date:
            raise ValidationError('Please enter a valid date.')

        # Custom validation logic for the expiry_date field
        # ...

        return expiry_date
