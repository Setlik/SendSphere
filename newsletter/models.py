from django.conf import settings
from django.db import models


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О.")
    comment = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Содержание")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("running", "Запущена"),
        ("completed", "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="created", verbose_name="Статус"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Сообщение",
    )
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.message:
            return f"Рассылка {self.message.subject} ({self.status})"
        else:
            return f"Рассылка (Без сообщения) ({self.status})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )
    attempt_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )
    status = models.CharField(
        max_length=20,
        choices=[("success", "Успешно"), ("failed", "Не успешно")],
        verbose_name="Статус",
    )
    response = models.TextField(blank=True, verbose_name="Ответ почтового сервера")

    def __str__(self):
        return f"Попытка {self.id} для рассылки {self.mailing.id}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.name
