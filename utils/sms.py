from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from TourCompass import settings


def send_code(recipient_email, code):
    subject = 'Tour-Compass Code'
    html_content = render_to_string('../templates/send_code.html', {'code': code})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [recipient_email])
    email.attach_alternative(html_content, 'text/html')
    email.send()


def send_password(recipient_email, password):
    subject = 'Tour-Compass Password'
    html_content = render_to_string('../templates/password.html', {'password': password})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [recipient_email])
    email.attach_alternative(html_content, 'text/html')
    email.send()
