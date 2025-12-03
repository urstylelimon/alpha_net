import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import transcription.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alpha_net.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            transcription.routing.websocket_urlpatterns
        )
    ),
})