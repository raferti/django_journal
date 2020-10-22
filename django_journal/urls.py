from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static


urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('journal/', include('journal.urls')),
    path('mailing/', include('mailing.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('api.v1.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
