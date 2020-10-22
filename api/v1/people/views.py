from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from api.v1.people.serializers import UserSerializer, UserTeacherDetailSerializer, UserStudentDetailSerializer, \
    UserStudentCreateSerializer
from api.v1.permissions import IsTeacher, IsTeacherOrOwnerUser
from django_journal.settings import TEACHER, STUDENT
from people.models import User


class TeacherListView(generics.ListAPIView):
    """Вывод всех учителей в школе."""
    queryset = User.objects.filter(user_status=TEACHER)
    serializer_class = UserSerializer


class TeacherProfileView(generics.RetrieveAPIView):
    """Вывод информации о учителе."""
    queryset = User.objects.filter(user_status=TEACHER)
    serializer_class = UserTeacherDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacher)


class StudentProfileView(generics.RetrieveUpdateAPIView):
    """Обновление или вывод информации о студенте."""
    queryset = User.objects.filter(user_status=STUDENT)
    serializer_class = UserStudentDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrOwnerUser)


class StudentCreateView(generics.CreateAPIView):
    """Создание студента."""
    queryset = User.objects.all()
    serializer_class = UserStudentCreateSerializer
    permission_classes = (IsAuthenticated, IsTeacher)


class LoginView(APIView):
    """Авторизация пользователя."""
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                token = Token.objects.get(user=user)
            except ObjectDoesNotExist:
                token = Token.objects.create(user=user)
            return Response({'Token': str(token)})
