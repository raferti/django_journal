from django import forms

from mailing.models import Mailing


class MailingCreateForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['name', 'subject', 'message', 'to_users']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название рассылки'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Заголовок сообщения'}),
            'message': forms.Textarea(attrs={'placeholder': 'Текст сообщения'}),
        }
