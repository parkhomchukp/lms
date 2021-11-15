from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

from student.token_generator import TokenGenerator
from django.utils.http import urlsafe_base64_encode


def send_registration_email(request, user_instance):
    current_domain = get_current_site(request).domain
    mail_subject = "Activate your LMS profile"
    message = render_to_string(
        "emails/registrations_email.html",
        {
            "user": user_instance,
            "domain": current_domain,
            "uid": urlsafe_base64_encode(force_bytes(user_instance.pk)),
            "token": TokenGenerator().make_token(user_instance),
        },
    )
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=["user.email"],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)
