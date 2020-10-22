from rest_framework import permissions
from rest_framework.permissions import BasePermission

from django_journal.settings import TEACHER
from journal.models import Lesson
from people.models import Teacher


class IsTeacher(BasePermission):
    """Только учитель."""
    def has_permission(self, request, view):
        return request.user.user_status == TEACHER


class IsTeacherOrOwnerUser(BasePermission):
    """
    Учитель или пользователь владелец.
    GET(просмотр) - все учителя или пользователь владелец.
    Другие методы (UPDATE) - только учителя.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and \
                (request.user.user_status == TEACHER or obj.id == request.user.id):
            return True
        return request.user.user_status == TEACHER


class IsOwnerUser(BasePermission):
    """Только тот учитель кто создал оценку."""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.teacher


class IsTeacherLesson(BasePermission):
    """Учитель который ведет урок."""
    def has_permission(self, request, view):
        teacher = Teacher.objects.prefetch_related('lessons') \
            .filter(user=request.user, lessons=view.kwargs.get('lesson_id', None)).exists()
        lesson_in_group = Lesson.objects\
            .filter(grade__group=view.kwargs.get('group_id', None), id=view.kwargs.get('lesson_id', None))
        return request.user.user_status == TEACHER and teacher and lesson_in_group
