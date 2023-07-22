from django.test import TestCase
from django.urls import reverse

from .models import Job

# Create your tests here.

class JobTestCase(TestCase):
    def setUp(self):
        self.job = Job.objects.create(
            title='New Job',
            description='Job 1',
            sector='commercial',
            contract_type='temporary',
            pay=40,
            employer_name='Google',
            incorporation_number='jdj343',
            website='https:www.abc.abc',
            expiry_date='2023-06-30',
            application_url='https://www.abc.abc',
            is_published=True,
        )

    def test_job_list_view(self):
        response = self.client.get(reverse('jobs:job_listing'))
        self.assertEqual(response.status_code, 200)

    def test_job_count(self):
        jobs = Job.objects.all().count()
        self.assertEqual(jobs, 1)

    def test_job_id(self):
        job = Job.objects.get(pk=self.job.pk)
        self.assertEqual(job.title, 'New Job')

    def test_get_absolute_url(self):
        job = Job.objects.get(pk=self.job.pk)
        expected_url = job.get_absolute_url()
        self.assertEqual(expected_url, f'/jobs/{job.pk}/')
