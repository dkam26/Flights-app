from django.core.mail import send_mail
import datetime

def send_notification_email(name,email,date,origin,destination):
    recipient_list = [email,]
    travel_date = date.split("T")[0]
    travel_time = date.split("T")[1][:-1]
    send_mail(name,"Hey "+name+" your scheduled flight from "+origin+" to "+destination+" on the date "+travel_date+" and time "+travel_time+" is tomorrow!",'deo.kamara@andela.com',recipient_list,fail_silently=False)