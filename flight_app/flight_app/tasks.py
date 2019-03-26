from celery import shared_task
from __future__ import absolute_import, unicode_literals
from user.models import User

@shared_task
def send_notification_mail(user_id, context):
    user = User.objects.filter(pk=user_id)
    if user:
        print(user)
    else:
        print('not found')