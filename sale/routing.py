from django.urls import path
from basic import consumers

# TODO: rotas do websocket

urlrouter = [
    path('chat/', consumers.ChatConsumer.as_asgi())
]
