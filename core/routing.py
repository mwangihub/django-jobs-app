from channels.auth import (AuthMiddleware, AuthMiddlewareStack)
from channels.routing import (
    URLRouter,
    ProtocolTypeRouter
)
from channels.security.websocket import (
    AllowedHostsOriginValidator
)
from django.conf.urls import url
from django.urls import re_path,path


application = ProtocolTypeRouter({
    'websocket' : AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                
                ]
            )
        )
    )
})