from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email(data):
    # email = EmailMessage(
    #     data['email_subject'], 
    #     data['email_body'] ,
    #     settings.EMAIL_HOST, 
    #     data['to_emails'],
    #     html_message = data['html_message']
    # )
    # email.send()
    send_mail(data['email_subject'], 
        data['email_body'] ,
        settings.EMAIL_HOST, 
        data['to_emails'],
        html_message = data['html_message']
        )


def temp_url(request, user, reverse_name, mail_body, token):

    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))    
    current_site = get_current_site(request=request).domain
    relativeLink = reverse('account:'+reverse_name)

    absurl = 'http://'+current_site + relativeLink
    url    = absurl +"?uidb64=" + uidb64 + "&token=" + token
    # email_body = f'Hello, \n Use link below to {mail_body}  \n'
    context = {
        'username': user.username,
        'temp_url': url,
        'mail_body': mail_body
    }
    html_message = render_to_string('mail_template.html', context=context)
    email_body = strip_tags(html_message)
    data = {'email_body': email_body, 'to_emails': [user.email,],'email_subject': mail_body, 'html_message':html_message}
    return data