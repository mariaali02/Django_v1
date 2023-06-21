""""
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home)
]"""
from django.contrib import admin
from django.urls import path
from flipcart import views
from .views import signin,hello_world,signout,home,signup

urlpatterns = [
    # Other URL patterns
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('hello/', hello_world, name='hello_world'),
    path('signout/', views.signout, name='signout'),
    
]

