from django.core.mail import send_mail

def send_notification_email(name,email,message):
    recipient_list = [email,]
    send_mail(name,message+" \n "+email,'deo.kamara@andela.com',recipient_list,fail_silently=False)