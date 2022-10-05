from django.urls import path
from .consumers import MainConsumer

ws_urlpatterns = [
    path('ws/main/', MainConsumer.as_asgi())
]