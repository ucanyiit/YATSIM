from django.urls import path
from yatsim.consumer import RoomConsumer

websocket_urlpatterns = [path("ws/play/<int:room_id>/", RoomConsumer.as_asgi())]
