import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task

from .models import LoginNote, Member

@shared_task
def note_login(member_id):
    # find member
    member = Member.objects.get(pk=member_id)
    note = LoginNote.objects.create(member=member)
    note.save()
    return 'login_note for {} created'.format(member.full_name)
