from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from .services import StripeGateway
from funky_time import years_from
from datetime import datetime


class Member(models.Model):
    gift_aid_help_text = (
        "I would like The UK Government to increase the value of my donation by as much as 25% at no "
        "cost to me!<br /><br />I want to Gift Aid my donation, and any donations I make in the "
        "future or have made in the past 4 years, to Geek.Zone. I am a UK taxpayer and understand "
        "that if I pay less Income Tax and/or Capital Gains Tax than the amount of Gift Aid claimed "
        "on all my donations in that tax year it is my responsibility to pay any difference.<br "
        "/><br />I will notify Geek.Zone if I:<ul><li>want to cancel this declaration</li><li>change "
        "my name or home address</li><li>no longer pay sufficient tax on my income and/or capital "
        "gains</li></ul> "
    )

    full_name = models.CharField(max_length=255, verbose_name="Full name")
    preferred_name = models.CharField(
        max_length=255,
        verbose_name="Preferred name",
        help_text="What should we call you?",
    )
    email = models.EmailField(max_length=254)
    birth_date = models.DateField(
        verbose_name="Date of birth",
        help_text="When did you begin your glorious adventure around or local star?",
    )
    constitution_agreed = models.BooleanField(
        help_text="I have read and agree to abide by the <a "
        'href="http://geek.zone/constitution">Geek.Zone/Constitution</a>. ',
        default=False,
    )
    constitutional_email = models.BooleanField(
        help_text="I am happy to receive emails that relate to constitutional matters",
        default=False,
    )
    constitutional_post = models.BooleanField(
        help_text="I am happy to receive letters that relate to constitutional matters",
        default=False,
    )

    stripe_customer_id = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to="images/",
        blank=True,
        verbose_name="Selfie",
        help_text="Strike a geek pose and give us your best shot! This will be used on your GZID card",
    )
    telephone = models.CharField(
        max_length=255, blank=True, verbose_name="Phone number"
    )
    minecraft_username = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Minecraft username",
        help_text="What is your Minecraft Java Edition username? Let us know so that you can join us on Geek.Zone/Minecraft!",
    )
    address_1 = models.CharField(
        max_length=255, blank=True, verbose_name="Address line one"
    )
    address_postcode = models.CharField(
        max_length=10, blank=True, verbose_name="Postcode"
    )
    gift_aid = models.BooleanField(
        default=False, verbose_name="Gift aid", help_text=gift_aid_help_text
    )
    gdpr_likeness = models.BooleanField(
        default=False,
        verbose_name="Likeness",
        help_text="May we use photos, videos or voice recordings of you in our publications?",
    )
    # JDG NB: updates = news (event info etc), notifications = system messages (2FA etc)
    gdpr_sms_updates = models.BooleanField(
        default=False,
        verbose_name="SMS updates",
        help_text="May we sent you updates, like event information, via SMS?",
    )
    gdpr_sms_notifications = models.BooleanField(
        default=False,
        verbose_name="SMS notifications",
        help_text="May we send you system notifications by SMS? This includes 2FA notifications",
    )
    gdpr_email_updates = models.BooleanField(
        default=False,
        verbose_name="Email updates",
        help_text="May we send you updates, like event information, via email?",
    )
    gdpr_email_notifications = models.BooleanField(
        default=False,
        verbose_name="Email notifications",
        help_text="May we send you system notifications by email? "
        "This is required to participate in Geek.Zone Elections",
    )
    gdpr_telephone_updates = models.BooleanField(
        default=False,
        verbose_name="Phone updates",
        help_text="May we call you with updates, like event information?",
    )
    gdpr_telephone_notifications = models.BooleanField(
        default=False,
        verbose_name="Phone notifications",
        help_text="May we call you to notify you of system messages? This includes 2FA",
    )
    gdpr_post_updates = models.BooleanField(
        default=False,
        verbose_name="Post updates",
        help_text="May we send you updates, like event information, via post?",
    )
    gdpr_post_notifications = models.BooleanField(
        default=False,
        verbose_name="Post notifications",
        help_text="May we send you system notifications by post? This includes 2FA and voting notifications",
    )
    # MVP only
    renewal_date = models.DateTimeField(
        null=True,
        verbose_name="Membership renewal date",
    )
    email_verified = models.BooleanField(
        default=False,
        verbose_name="Email verified",
    )

    class Meta:
        verbose_name = "member"
        verbose_name_plural = "members"
        permissions = (
            ("has_membership", "Member has paid"),
            ("reminder_email_24hr", "New member sent 24hr payment email"),
            ("reminder_email_72hr", "New member sent 72hr payment email"),
        )

    @staticmethod
    def create(full_name, email, password, birth_date, preferred_name=None):
        stripe_gateway = StripeGateway()
        stripe_customer_id = stripe_gateway.upload_member(email)

        preferred_name = preferred_name if preferred_name else full_name
        with transaction.atomic():
            user = User.objects.create_user(
                username=email, password=password, email=email
            )
            return Member.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                birth_date=birth_date,
                preferred_name=preferred_name,
                constitution_agreed=True,
                constitutional_email=True,
                constitutional_post=True,
                stripe_customer_id=stripe_customer_id,
            )

    def __str__(self):
        return self.full_name


class Membership(models.Model):
    # todo: What should the on_delete be?
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    last_payment_time = models.DateTimeField(null=True)
    payment_status = models.CharField(max_length=255, null=True)


class FailedPayment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    stripe_event_type = models.CharField(max_length=255)


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
