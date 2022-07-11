"""
ASGI config for shixun project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing  # 这个文件后续会说，你先写上。

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shixun.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": URLRouter(routing.websocket_urlpatterns),
})
