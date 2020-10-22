from django.urls import path

from api.v1.journal.views import JournalGroupListView, JournalStudentListView, ScoreView


urlpatterns = [
    path('<int:group_id>/<int:lesson_id>/', JournalGroupListView.as_view()),
    path('student-lk/', JournalStudentListView.as_view()),
    path('score/<int:pk>/', ScoreView.as_view())
]
