"""
ASGI config for easywork_be project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from messaging.consumers import *

from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easywork_be.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    'http' : get_asgi_application(),  
    'websocket' : AuthMiddlewareStack(
        URLRouter (
            [path('message/notification_testing/', NotificationConsumer.as_asgi() )]
        )
    ) 
})
