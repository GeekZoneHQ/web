from django.db import models
from django.urls import reverse


# Create your models here.


class Job(models.Model):
    SECTOR_CHOICES = [("commercial", "Commercial"), ("charity", "Charity")]

    CONTRACT_TYPE_CHOICES = [
        ("voluntary", "Voluntary"),
        ("temporary", "Temporary"),
        ("fixed_term_contract", "Fixed Term Contract"),
        ("part_time_permanent", "Part-time Permanent"),
        ("full_time_permanent", "Full-time Permanent Employed"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    contract_type = models.CharField(max_length=40, choices=CONTRACT_TYPE_CHOICES)
    pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    employer_name = models.CharField(max_length=100)
    incorporation_number = models.CharField(max_length=20, blank=True)
    website = models.URLField(max_length=200)
    expiry_date = models.DateField()
    application_url = models.URLField(max_length=200)
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    published_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def is_expired(self):
        from datetime import date

        return date.today() > self.expiry_date

    def get_absolute_url(self):
        return reverse("jobs:job_detail", kwargs={"pk": self.pk})
