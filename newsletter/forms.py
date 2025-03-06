from django import forms
from .models import Recipient, Message, Mailing


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ('email', 'full_name', 'comment')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'body')

class MailingForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        label='Получатели',
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Mailing
        fields = ('start_time', 'end_time', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['recipients'].initial = self.instance.recipients.all()

    def save(self, commit=True):
        mailing = super().save(commit=False)
        if commit:
            mailing.save()
        mailing.recipients.set(self.cleaned_data['recipients'])
        return mailing