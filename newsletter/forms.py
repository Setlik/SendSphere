from django import forms
from tinymce.widgets import TinyMCE

from .models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ("email", "full_name", "comment")


class MessageForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = Message
        fields = ["subject", "body"]


class MailingForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        label="Получатели",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        required=False,
    )

    start_time = forms.DateTimeField(
        label="Дата и время первой отправки",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    end_time = forms.DateTimeField(
        label="Дата и время окончания отправки",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "recipients", "message", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["recipients"].initial = self.instance.recipients.all()
