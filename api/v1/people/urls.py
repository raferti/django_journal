from django.urls import path

from api.v1.people.views import TeacherListView, TeacherProfileView, StudentProfileView, StudentCreateView


urlpatterns = [
    path('teacher/', TeacherListView.as_view()),
    path('teacher/<int:pk>/', TeacherProfileView.as_view()),
    path('create-student/', StudentCreateView.as_view()),
    path('student/<int:pk>/', StudentProfileView.as_view()),
]
