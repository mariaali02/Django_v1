from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('flipcart.urls')),
    path('apitest/', include('apitest.urls')), 
    #path('api/', include('accounts.urls')),  # Include the app's URLs
    path('apitest/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
