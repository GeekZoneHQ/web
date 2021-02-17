from celery import shared_task
from celery.utils.log import get_task_logger
from .email import send_email

logger = get_task_logger(__name__)


@shared_task(name="task_send_email")
def task_send_email(to_name, to_email, subject, body):
    logger.info("Email on its way!")
    return send_email(to_name, to_email, subject, body)
