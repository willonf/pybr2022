"""
ASGI config for sale project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

# TODO: Configuração do websocket no ASGI
# O Django já tem um mecanismo para aplicações de alta escalabilidade que é esse arquivo ASGI
# Aqui configuramos quais protocolos a aplicação irá atender, nesse caso WS e HTTP

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from sale import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sale.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(routing.urlrouter)
})
