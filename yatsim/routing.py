from django.urls import path
from yatsim.consumer import RoomConsumer

websocket_urlpatterns = [
    path("ws/play/<str:room_id>/<str:token>", RoomConsumer.as_asgi())
]
