from django.core.mail import send_mail
import datetime

def send_notification_email(name,email,date,origin,destination):
    recipient_list = [email,]

    send_mail(name,"Hey "+name+" your scheduled flight from "+origin+" to "+destination+" on the date "+date+" is tomorrow !",'deo.kamara@andela.com',recipient_list,fail_silently=False)