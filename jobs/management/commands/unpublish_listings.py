import datetime
from django.core.management.base import BaseCommand
from jobs.models import Job


class Command(BaseCommand):
    help = "Unpublish expired job listings"

    def handle(self, *args, **options):
        expired_date = datetime.date.today() - datetime.timedelta(days=30)
        expired_listings = Job.objects.filter(created__lt=expired_date)
        expired_listings.update(is_published=False)
