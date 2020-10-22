from django.urls import path, include

from api.v1.people.views import LoginView

urlpatterns = [
    path('people/', include('api.v1.people.urls')),
    path('group/', include('api.v1.group.urls')),
    path('journal/', include('api.v1.journal.urls')),
    path('login/', LoginView.as_view()),
]
