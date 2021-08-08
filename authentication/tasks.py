
from random import randint
from celery import shared_task

from django.core.mail import EmailMessage
from django.apps import apps
from django.template.loader import get_template
from django.conf import settings


@shared_task
def send_email_confirmation(user_email):
    """ Отправить письмо с подтверждением email при регистрации пользователя. """

    user_model = apps.get_model('authentication', 'User')
    confirmation_codes_model = apps.get_model('authentication', 'ConfirmationCodes')
    user = user_model.objects.get(email=user_email)
    code = randint(1000, 9999)
    confirmation_codes_model.objects.create(
        user=user,
        code=code,
    )
    message = get_template("emails/email_conf.html").render(
        user.get_serialized_data(),
    )
    mail = EmailMessage(
        subject="[Petme] Подтверждение почты",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    mail.send()
