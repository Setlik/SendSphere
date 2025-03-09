from datetime import timedelta

from django.utils import timezone

from .models import CustomUser


def delete_unconfirmed_users():
    # Ищем и удаляем пользователей, не активированных за последние 5 минут
    time_limit = timezone.now() - timedelta(minutes=5)
    unconfirmed_users = CustomUser.objects.filter(
        is_active=False, created_at__lt=time_limit
    )
    unconfirmed_users.delete()
