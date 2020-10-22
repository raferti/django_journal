from django.urls import path

from people.views import TeacherListView, TeacherDetailView, StudentDetailView, StudentLkDetailView, \
    StudentUpdateView, StudentCreateView


urlpatterns = [
    path('teacher/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/info/<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('student/add/', StudentCreateView.as_view(), name='student_add'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('student/info/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/', StudentLkDetailView.as_view(), name='student_lk'),
    ]
