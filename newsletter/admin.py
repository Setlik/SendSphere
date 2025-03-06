from django.contrib import admin
from .models import Recipient, Message, Mailing, MailingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'comment']
    list_filter = ['email']
    search_fields = ['email', 'full_name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    search_fields = ('subject', 'body')

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'status', 'message')
    list_filter = ('status', 'message')
    search_fields = ('message__subject',)

@admin.register(MailingAttempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_date', 'status')
    list_filter = ('status', 'mailing')
    search_fields = ('mailing__id',)
