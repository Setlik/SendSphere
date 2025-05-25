# from celery import shared_task, result
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Mailing, MailingAttempt
# from django.shortcuts import get_object_or_404
#
#
# была попытка подключить celery для асинхронности
# @shared_task
# def send_mailing_task(mailing_id):
#     """Отправляет рассылку всем получателям."""
#     mailing = get_object_or_404(Mailing, pk=mailing_id)
#     recipients = mailing.recipients.all()
#
#     for recipient in recipients:
#         try:
#             send_mail(
#                 mailing.message.subject,
#                 mailing.message.body,
#                 settings.EMAIL_HOST_USER,
#                 [recipient.email],
#                 fail_silently=False,
#             )
#             print(f"Результат send_mail: {result}")
#
#             MailingAttempt.objects.create(
#                 mailing=mailing,
#                 status='success',
#                 response='Сообщение успешно отправлено',
#             )
#
#
#         except Exception as e:
#             MailingAttempt.objects.create(
#                 mailing=mailing,
#                 status='failed',
#                 response=str(e),
#             )
#             print(f'Ошибка при отправке сообщения получателю {recipient.email}: {str(e)}')
