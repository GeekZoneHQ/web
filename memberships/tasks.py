from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from django.contrib.auth.models import Permission, User
from memberships.models import Member

from .email import send_email

logger = get_task_logger(__name__)


@shared_task
def task_send_email(
    to_name, to_email, subject, body
):  # where possible, to_name should be preferred name
    logger.info("Email on its way!")
    return send_email(to_name, to_email, subject, body)


@shared_task
def task_payment_check(id):
    try:
        member = Member.objects.get(id=id)
        user = User.objects.get(id=member.user_id)
        if not user.has_perm("memberships.has_membership"):
            if user.has_perm("memberships.reminder_email_72hr"):
                logger.info("New user has not paid in 120 hours.")
                subject = "120hr email subject"
                body = "120hr email body"
                # todo: delete user
            elif user.has_perm("memberships.reminder_email_24hr"):
                logger.info("New user has not paid in 72 hours.")
                perm = Permission.objects.get(codename="reminder_email_72hr")
                user.user_permissions.add(perm)
                exec_time = datetime.utcnow() + timedelta(hours=46)
                task_payment_check.apply_async(args=(member.id,), eta=exec_time)
                subject = "72hr email subject"
                body = "72hr email body"
            else:
                logger.info("New user has not paid in 24 hours.")
                perm = Permission.objects.get(codename="reminder_email_24hr")
                user.user_permissions.add(perm)
                exec_time = datetime.utcnow() + timedelta(hours=48)
                task_payment_check.apply_async(args=(member.id,), eta=exec_time)
                subject = "24hr email subject"
                body = "24hr email body"

            task_send_email(member.preferred_name, member.email, subject, body)

    except Member.DoesNotExist:
        # todo: should anything be done if the user is not found?
        logger.info(f"User with id: {id} not found.")
