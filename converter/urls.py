from django.urls import path
from . import views


urlpatterns = [
    path('', views.GenericView.as_view(), name='index'),
    path('convert/', views.convert, name='convert'),
    path('delete/', views.download_and_delete, name='delete'),
]