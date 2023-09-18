from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from tasks import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [
            path("ws/updates/", consumers.RealTimeUpdatesConsumer.as_asgi()),
        ]
    ),
})
