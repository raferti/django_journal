from django.db import models
from django.urls import reverse_lazy

from people.models import User


class Mailing(models.Model):
    """Информационные рассылки."""
    name = models.CharField(max_length=150, verbose_name='Название рассылки')
    subject = models.CharField(max_length=150, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Текст сообщения')
    from_user = models.ForeignKey(User, related_name='mailing_from', on_delete=models.CASCADE, verbose_name='Отправитель')
    to_users = models.ManyToManyField(User, related_name='mailing_to', verbose_name='Получатели')
    created = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('mailing_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
