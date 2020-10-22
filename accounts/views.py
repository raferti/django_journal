from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from django_journal.settings import STUDENT


class UserTypeRedirectView(LoginRequiredMixin, RedirectView):
    """
    Редирект сразу после прохождения авторизации.
    В зависимости от типа авторизованного пользователя (учитель, студент),
    перенаправляет пользователя на соответсвующий url.
    """
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.user_status == STUDENT:
            return reverse_lazy('student_lk')
        else:
            return reverse_lazy('group_student_list')
