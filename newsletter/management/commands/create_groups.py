from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        recipient_content_type = ContentType.objects.get_for_model(
            apps.get_model("newsletter", "Recipient")
        )

        user_content_type = ContentType.objects.get_for_model(
            apps.get_model("auth", "User")
        )

        mailing_content_type = ContentType.objects.get_for_model(
            apps.get_model("newsletter", "Mailing")
        )

        newsletter_managers_group = Group.objects.create(name="Newsletter Managers")

        recipient_permissions = Permission.objects.filter(
            content_type=recipient_content_type,
            codename__in=[
                "view_recipient",
                "add_recipient",
                "change_recipient",
                "delete_recipient",
            ],
        )

        user_permissions = Permission.objects.filter(
            content_type=user_content_type,
            codename__in=[
                "change_user",
            ],
        )

        mailing_permissions = Permission.objects.filter(
            content_type=mailing_content_type,
            codename__in=[
                "change_mailinglist",
            ],
        )

        all_permissions = recipient_permissions | user_permissions | mailing_permissions

        newsletter_managers_group.permissions.set(all_permissions)

        self.stdout.write(
            self.style.SUCCESS("Successfully created groups and permissions")
        )
