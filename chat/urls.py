from django.urls import path
from . import views 


urlpatterns = [
    path('', views.indext, name='indext'),
    path('room/<str:room_name>/', views.room, name='room'),
]