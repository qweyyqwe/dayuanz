# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : asgi.py
# @Software: PyCharm


# django ——不支持asgi
"""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from . import routing
from channels.auth import AuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dyz_account.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
})
"""

import os
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import routing  # 这个文件后续会说，你先写上。

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_platform.settings')
django.setup()

# application = ProtocolTypeRouter({
#   "http": AsgiHandler(),
#   "websocket": URLRouter(routing.websocket_urlpatterns),
# })


application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": URLRouter(routing.websocket_urlpatterns),
})

# application = ProtocolTypeRouter({"http": get_asgi_application(), "websocket": AuthMiddlewareStack(
#   URLRouter(chat.routing.websocket_urlpatterns)),  # 暂时只是 HTTP。（我们可以稍后添加其他协议。） })
