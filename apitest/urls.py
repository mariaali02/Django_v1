from rest_framework import routers
from django.urls import path, include
from django.contrib import admin
from apitest import views

urlpatterns = [
    
    # Include API endpoints from your views
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('UserProfile/',views.UserProfileListView.as_view(), name='userprofile-list'),
    path('UserProfile/<int:pk>/', views.UserProfileView.as_view(), name='userprofile-detail'),
    path('hello', views.Hello.as_view()),
    path('userdetail', views.UserDetail1.as_view()),
    path('registeruser/', views.registeruser.as_view(), name='registeruser'),
    path('SoftDeleteUser/', views.SoftDeleteUser.as_view(), name='SoftDeleteUser'),
    path('SignIn/', views.SignIn.as_view(), name='SignIn'),
    path('UserDashboard/', views.UserDashboard, name='UserDashboard'),
    path('SuperuserDashboard/', views.SuperuserDashboard, name='SuperuserDashboard'),
    path('SignOut/', views.SignOut.as_view(), name='SignOut'),
    path('logout/', views.logout ,name='logout'),

]