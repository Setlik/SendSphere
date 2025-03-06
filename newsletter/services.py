from django.conf import settings
from django.core.mail import send_mail
from .models import MailingAttempt


def send_mailing(mailing):
    recipients = mailing.recipients.all()  # Получаем список получателей

    for recipient in recipients:
        try:
            send_mail(
                mailing.subject,
                mailing.message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                status='successful',
                server_response='Письмо успешно отправлено'
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='failed',
                server_response=str(e)
            )
