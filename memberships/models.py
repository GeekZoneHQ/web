from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from .services import StripeGateway


COUNTRY_CHOICES = ["countries"]




class Member(models.Model):
    full_name = models.CharField(max_length=255)
    preferred_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    birth_date = models.DateField()
    constitution_agreed = models.BooleanField()
    stripe_customer_id = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="images/")
    telephone = models.CharField(max_length=255)
    minecraft_username = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_postcode = models.CharField(max_length=10)
    gift_aid = models.BooleanField()
    gdpr_likeness = models.BooleanField()
    gdpr_sms_updates = models.BooleanField()
    gdpr_sms_notifications = models.BooleanField()
    gdpr_email_updates = models.BooleanField()
    gdpr_email_notifications = models.BooleanField()
    gdpr_telephone_updates = models.BooleanField()
    gdpr_telephone_notifications = models.BooleanField()
    gdpr_post_updates = models.BooleanField()
    gdpr_post_notifications = models.BooleanField()


    class Meta:
        verbose_name = "member"
        verbose_name_plural = "members"

    @staticmethod
    def create(full_name, email, password, birth_date, preferred_name=None):
        stripe_gateway = StripeGateway()
        stripe_customer_id = stripe_gateway.upload_member(email)

        preferred_name = preferred_name if preferred_name else full_name
        with transaction.atomic():
            user = User.objects.create_user(username=email, password=password)
            return Member.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                birth_date=birth_date,
                preferred_name=preferred_name,
                constitution_agreed=True,
                stripe_customer_id=stripe_customer_id,
            )

    def __str__(self):
        return self.full_name


# todo: store the membership type (sand, space)
class Membership(models.Model):
    # todo: What should the on_delete be?
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
