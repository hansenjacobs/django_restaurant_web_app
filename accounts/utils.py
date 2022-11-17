from django.core.mail import EmailMessage
from .models import User
from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


def get_user_dashboard(user):
    dashboards = {
        User.VENDOR: 'vendordashboard',
        User.CUSTOMER: 'customerdashboard',
    }

    dashbaord = None

    try:
        dashboard = dashboards[user.role]
    except:
        if user.is_superadmin:
            dashboard = '/admin'

    return dashboard


def user_is_customer(user):
    if user.role == User.CUSTOMER:
        return True
    else:
        raise PermissionDenied


def user_is_vendor(user):
    if user.role == User.VENDOR:
        return True
    else:
        raise PermissionDenied


def send_verification_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Please Activate You Account'
    message = render_to_string('accounts/emails/account_verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email],
                        from_email='Python Project FoodOnline <support@shopjtx.com>')
    mail.send()
