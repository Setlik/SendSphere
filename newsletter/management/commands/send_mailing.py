from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from newsletter.models import Mailing


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--mailing_id",
            type=int,
            help="ID of the mailing to send",
        )

    def handle(self, *args, **options):
        mailing = Mailing.objects.get(id=options["mailing_id"])
        recipients = mailing.recipients.all()

        for recipient in recipients:
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    settings.EMAIL_HOST_USER,
                    [recipient.email],
                    fail_silently=False,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Сообщение отправлено {recipient.email}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Ошибка при отправке сообщения {recipient.email}: {str(e)}"
                    )
                )
