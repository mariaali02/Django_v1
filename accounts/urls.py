from django.urls import path
from accounts import views



urlpatterns = [
    path('register/', views.registeruser, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
]
