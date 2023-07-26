from rest_framework import routers
from django.urls import path, include
from django.contrib import admin
from API import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
path('', include(router.urls)),
path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),