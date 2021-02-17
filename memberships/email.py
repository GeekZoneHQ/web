from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_email(to_name, to_email, subject, body):
    context = {
        'name': to_name,
        'email': to_email,
        'body': body
    }
    email_body = render_to_string('email_message.html', context)

    email = EmailMessage(
        subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [to_name],
    )
    return email.send(fail_silently=False)
