from channels.routing import ProtocolTypeRouter, URLRouter
import amazone.routing
import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazone.settings')



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            amazone.routing.websocket_urlpatterns
        )
    ),
})
