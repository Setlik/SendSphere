from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Contact, Mailing, MailingAttempt, Message, Recipient


class HomeView(View):
    def get(self, request):
        cache_key = "home_view_stats"
        stats = cache.get(cache_key)

        if stats is None:
            total_mailings = Mailing.objects.count()
            active_mailings = Mailing.objects.filter(status="running").count()
            unique_recipients = Recipient.objects.count()
            stats = {
                "total_mailings": total_mailings,
                "active_mailings": active_mailings,
                "unique_recipients": unique_recipients,
            }

            cache.set(cache_key, stats, timeout=300)

        return render(request, "newsletter/home.html", stats)


class CreateMailingView(View):
    def get(self, request):
        form = MailingForm()
        messages_list = Message.objects.all()
        all_recipients = Recipient.objects.all()

        create_message_url = reverse("message_create")
        create_recipient_url = reverse("recipient_create")

        return render(
            request,
            "newsletter/create_mailing.html",
            {
                "form": form,
                "messages": messages_list,
                "recipients": all_recipients,
                "create_message_url": create_message_url,
                "create_recipient_url": create_recipient_url,
            },
        )

    def post(self, request):
        form = MailingForm(request.POST, request.FILES)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user
            mailing.status = "created"
            mailing.save()

            selected_recipients = form.cleaned_data["recipients"]
            mailing.recipients.set(selected_recipients)

            return redirect("mailing_list")
        else:
            messages_list = Message.objects.all()
            all_recipients = Recipient.objects.all()
            create_message_url = reverse("message_create")
            create_recipient_url = reverse("recipient_create")
            return render(
                request,
                "newsletter/create_mailing.html",
                {
                    "form": form,
                    "messages": messages_list,
                    "recipients": all_recipients,
                    "create_message_url": create_message_url,
                    "create_recipient_url": create_recipient_url,
                },
            )


class MailingStartView(View):
    def get(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, pk=mailing_id)
        mailing.status = "running"
        mailing.save()
        return redirect("mailing_detail", mailing_id=mailing_id)


def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, id=pk)
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

            MailingAttempt.objects.create(
                mailing=mailing,
                status="success",
                response="Сообщение успешно отправлено",
            )

            messages.success(
                request, f"Сообщение отправлено получателю {recipient.email}"
            )

        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status="failed",
                response=str(e),
            )
            messages.error(
                request,
                f"Ошибка при отправке сообщения получателю {recipient.email}: {str(e)}",
            )

    return redirect("mailing_list")


class UserMailingReportsView(LoginRequiredMixin, View):
    template_name = "newsletter/mailing_statistics.html"

    def get(self, request):
        user = request.user
        cache_key = f"user_report_{user.id}"
        user_report = cache.get(cache_key)

        if user_report is None:
            user_report = MailingAttempt.objects.filter(mailing__owner=user).aggregate(
                total_sent=Count("id"),
                successful_attempts=Count("id", filter=Q(status="success")),
                failed_attempts=Count("id", filter=Q(status="failed")),
            )
            cache.set(cache_key, user_report, timeout=300)

        context = {
            "user_report": user_report,
        }
        return render(request, self.template_name, context)


class ContactView(LoginRequiredMixin, View):
    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, "newsletter/contacts.html", {"contacts": contacts})

    def post(self, request):
        name = request.POST.get("name")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class RecipientListView(ListView):
    model = Recipient
    template_name = "newsletter/recipient/recipient_list.html"
    context_object_name = "recipients"


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "newsletter/recipient/recipient_create.html"
    success_url = reverse_lazy("recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "newsletter/recipient/recipient_update.html"
    success_url = reverse_lazy("recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "newsletter/recipient/recipient_delete.html"
    success_url = reverse_lazy("recipient_list")


class MessageListView(ListView):
    model = Message
    template_name = "newsletter/messages/message_list.html"
    context_object_name = "messages"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/messages/message_create.html"
    success_url = reverse_lazy("message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/messages/message_update.html"
    success_url = reverse_lazy("message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "newsletter/messages/message_delete.html"
    success_url = reverse_lazy("message_list")


class MailingListView(ListView):
    model = Mailing
    template_name = "newsletter/mailings/mailing_list.html"
    context_object_name = "mailings"


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailings/create_mailing.html"
    success_url = reverse_lazy("mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailings/mailing_update.html"
    success_url = reverse_lazy("mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "newsletter/mailings/mailing_delete.html"
    success_url = reverse_lazy("mailing_list")


class MailingDetailView(View):
    def get(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, pk=mailing_id)
        return render(
            request, "newsletter/mailings/mailing_detail.html", {"mailing": mailing}
        )
