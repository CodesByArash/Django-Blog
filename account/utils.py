from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils.crypto import get_random_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse



def send_email(data):
    email = EmailMessage(
        data['email_subject'], 
        data['email_body'] ,
        settings.EMAIL_HOST, 
        data['to_emails'],
    )
    email.send()


def temp_url(request, user, reverse_name, mail_body):
    token  = account_activation_token.make_token(user)
    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

    current_site = get_current_site(request=request).domain
    relativeLink = reverse(reverse_name)

    absurl = 'http://'+current_site + relativeLink
    email_body = f'Hello, \n Use link below to {email_body}  \n' + absurl +"?uidb64=" + uidb64 + "&token=" + token
    data = {'email_body': email_body, 'to_emails': [user.email,],'email_subject': {email_body}}
    return data