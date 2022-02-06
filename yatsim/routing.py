from django.urls import path

from yatsim.consumer import TicTacToeConsumer

websocket_urlpatterns = [
    path(r"^ws/play/(?P<room_code>\w+)/$", TicTacToeConsumer.as_asgi())
]
