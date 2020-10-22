from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.v1.group.serializers import GroupSerializer, GroupDetailSerializer
from api.v1.permissions import IsTeacher
from journal.models import GroupStudent


class GroupListView(generics.ListAPIView):
    """Вывод всех школьных классов."""
    queryset = GroupStudent.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsTeacher)


class GroupDetailView(generics.RetrieveAPIView):
    """Вывод информации о школьном классе."""
    queryset = GroupStudent.objects.all()
    serializer_class = GroupDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacher)
