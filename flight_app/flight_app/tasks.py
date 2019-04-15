from celery import shared_task
from celery.utils.log import get_task_logger
from flight_app.flight_app.mailer import send_notification_email
from datetime import datetime, timedelta

logger=get_task_logger(__name__)

# This is the decorator which a celery worker uses
@shared_task(name="send_notification_email_task")
def send_notification_email_task(name,email,date,origin,destination):
    logger.info("Sent email")
    
    return send_notification_email(name,email,date,origin,destination)

