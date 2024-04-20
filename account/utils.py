from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils.crypto import get_random_string



def send_email(data):
    # subject = "Verify your email"
    # message = f"Please verify your email using this link \n\n\n 127.0.0.1:8000/account/verify-email/{otp}"
    # email_from = settings.EMAIL_HOST
    # send_mail(subject,message, email_from, [email])
    email = EmailMessage(
        data['email_subject'], 
        data['email_body'] ,
        settings.EMAIL_HOST, 
        data['to_emails'],
    )
    email.send()

