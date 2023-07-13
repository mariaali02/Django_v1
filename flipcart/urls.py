""""
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home)
]"""
from django.contrib import admin
from django.urls import path
from flipcart import views
from . views import signin,hello_world,signout,home,signup,msg,page1,dlt,update

urlpatterns = [
    # Other URL patterns
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('hello/', hello_world, name='hello_world'),
    path('signout/', views.signout, name='signout'),
    path('msg/', views.msg, name='msg'),
    path('page1/', views.page1, name='page1'),
    path("<int:user_id>/dlt/", views.dlt, name="dlt"),
    path("<int:user_id>/update/", views.update, name="update"),
    
]



