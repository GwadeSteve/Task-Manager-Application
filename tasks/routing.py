
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from tasks import consumers

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r"ws/tasks/$", consumers.TaskConsumer.as_asgi()),
            ]
        )
    ),
})