from django.urls import path

from api.v1.group.views import GroupListView, GroupDetailView


urlpatterns = [
    path('', GroupListView.as_view()),
    path('<int:pk>/', GroupDetailView.as_view())
]