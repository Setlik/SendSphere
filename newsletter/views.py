from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RecipientForm, MessageForm, MailingForm
from .models import Mailing, Message, Recipient, MailingAttempt, Contact
from django.utils import timezone


class HomeView(View):
    def get(self, request):
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='running').count()
        unique_recipients = Recipient.objects.count()

        context = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_recipients': unique_recipients,
        }
        return render(request, 'newsletter/home.html', context)


class CreateMailingView(View):
    def get(self, request):
        messages = Message.objects.all()
        recipients = Recipient.objects.all()
        return render(request, 'newsletter/create_mailing.html', {'messages': messages, 'recipients': recipients})

    def post(self, request):
        message_id = request.POST.get('message')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        message = Message.objects.get(id=message_id)
        mailing = Mailing.objects.create(
            start_time=start_time,
            end_time=end_time,
            message=message,
            status='created'
        )
        mailing.recipients.set(request.POST.getlist('recipients'))
        mailing.save()
        return redirect('mailing_list')


def send_mailing(request, pk):
    mailing = Mailing.objects.get(id=pk)
    recipients = mailing.recipients.all()

    for recipient in recipients:
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.body,
                'your_email@example.com',
                [recipient.email],
                fail_silently=False,
            )

            # Создаем запись об успешной попытке
            Attempt.objects.create(
                mailing=mailing,
                status='success',
                response='Сообщение успешно отправлено',
            )

            messages.success(request, f'Сообщение отправлено получателю {recipient.email}')
        except Exception as e:
            # Создаем запись о неуспешной попытке
            Attempt.objects.create(
                mailing=mailing,
                status='failed',
                response=str(e),
            )
            messages.error(request, f'Ошибка при отправке сообщения получателю {recipient.email}: {str(e)}')

    return redirect('mailing_list')


class MailingStartView(View):
    def get(self, request, mailing_id):
        mailing = Mailing.objects.get(id=mailing_id)
        # Запускаем процесс отправки
        mailing.status = 'started'
        mailing.save()
        return redirect('mailing_detail', pk=mailing_id)


class MailingStatisticsView(View):
    def get(self, request):
        attempts = MailingAttempt.objects.all()
        return render(request, 'newsletter/mailing_statistics.html', {'attempts': attempts})


class ContactView(LoginRequiredMixin, View):
    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, "newsletter/contacts.html", {"contacts": contacts})

    def post(self, request):
        name = request.POST.get("name")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipient/list.html'
    context_object_name = 'recipients'


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient/create.html'
    success_url = '/clients/'


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient/update.html'
    success_url = '/clients/'


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'recipient/delete.html'
    success_url = '/clients/'


class MessageListView(ListView):
    model = Message
    template_name = 'мessage/list.html'
    context_object_name = 'мessages'

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'мessage/create.html'
    success_url = '/мessages/'

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'мessage/update.html'
    success_url = '/мessages/'

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'мessage/delete.html'
    success_url = '/мessages/'


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/list.html'
    context_object_name = 'mailings'

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/create.html'
    success_url = '/mailings/'

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/update.html'
    success_url = '/mailings/'

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/delete.html'
    success_url = '/mailings/'
