from django.urls import path
from . import views

urlpatterns = [
    path('monitors', views.create_monitor, name='create-monitor'),
    path('monitors/<str:device_id>/heartbeat', views.heartbeat, name='heartbeat'),
]