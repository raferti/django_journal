from django.urls import path, include

from .views import GroupStudentListView, GroupStudentDetailView, ScoreLessonListView, AddScore


urlpatterns = [
    path('people/', include('people.urls')),
    path('groups/', GroupStudentListView.as_view(), name='group_student_list'),
    path('group/<int:pk>/', GroupStudentDetailView.as_view(), name='group_student_detail'),
    path('<int:group_id>/<int:lesson_id>/', ScoreLessonListView.as_view(), name='score_lesson'),
    path('addscore/', AddScore.as_view(), name='add_score'),
]
