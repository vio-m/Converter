from django.contrib import admin
from django.urls import path, re_path, include
#from django.conf import settings
#from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('converter.urls')),
    re_path(r'^celery-progress/', include('celery_progress.urls', namespace="celery_progress")),
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)