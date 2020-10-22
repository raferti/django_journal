from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.v1.journal.serializers import ScoreSerializer
from api.v1.permissions import IsTeacherLesson, IsOwnerUser
from django_journal.settings import STUDENT
from journal.models import Score
from people.models import User


class JournalGroupListView(generics.ListCreateAPIView):
    """Вывод оценок класса по предмету, добавление оценки ученику."""
    serializer_class = ScoreSerializer
    permission_classes = (IsAuthenticated, IsTeacherLesson)

    def get_queryset(self):
        queryset = Score.objects.filter(group=self.kwargs['group_id'], lesson=self.kwargs['lesson_id'])

        start_date = self.request.query_params.get('start-date', None)
        end_date = self.request.query_params.get('end-date', None)
        if start_date and end_date:
            queryset = queryset.filter(created__gte=start_date, created__lte=end_date)
        return queryset


class ScoreView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр-обновление-удаление оценки студента."""
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = (IsAuthenticated, IsOwnerUser)


class JournalStudentListView(generics.ListAPIView):
    """Вывод оценок по всем предметам конкретного студента."""
    serializer_class = ScoreSerializer

    def get_queryset(self):
        student = get_object_or_404(User, username=self.request.user, user_status=STUDENT)
        queryset = Score.objects.filter(student=student)
        return queryset
