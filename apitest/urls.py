from rest_framework import routers
from django.urls import path, include
from django.contrib import admin
from apitest import views

urlpatterns = [
    # Include API endpoints from your views
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('hello', views.Hello.as_view()),
    path('userdetail', views.UserDetail1.as_view()),
    path('register/', views.registeruser, name='register'),
    path('Signin/', SignInView.as_view(), name='signin')
    #path('user_dashboar/', views.user_dashboar, name='user_dashboar'),
    #path('superuser_dashboard/', views.superuser_dashboard, name='superuser_dashboard'),
    path('logout/', views.userlogout, name='logout'),

]