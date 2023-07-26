""""
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home)
]"""
from rest_framework import routers
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from flipcart import views
from . views import signin,user_dashboar,signout,home,signup,msg,page1,dlt,update,change_password,superuser_dashboar

urlpatterns = [
    # Other URL patterns
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('user_dashboar/', views.user_dashboar, name='user_dashboar'),
    path('superuser_dashboar/',views.superuser_dashboar, name='superuser_dashboar'),
    path('signout/', views.signout, name='signout'),
    path('change_password/', views.change_password, name='change_password'),
    path('msg/', views.msg, name='msg'),
    path('page1/', views.page1, name='page1'),
    path("<int:user_id>/dlt/", views.dlt, name="dlt"),
    path("<int:user_id>/update/", views.update, name="update"),

]



