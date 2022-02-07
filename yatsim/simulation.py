import threading
import time
from threading import Lock

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from yatsim_dashboard.models import Room


class Simulation(threading.Thread):
    def __init__(self, room: Room):
        self.lock = Lock()
        self.room = room
        self.is_alive = True
        self.is_running = False
        self.channel_layer = get_channel_layer()
        self.period = 1
        super().__init__()

    # PERIODT
    def set_period(self, period):
        with self.lock:
            self.period = period

    def toggle_sim(self):
        with self.lock:
            self.is_running = not self.is_running

    def stop_sim(self):
        with self.lock:
            self.is_alive = False

    def run(self):
        self.is_running = True
        next_time = time.time()
        while self.is_alive:
            while self.is_running:
                # update wagons
                async_to_sync(self.channel_layer.group_send)(
                    str(self.room.id),
                    {
                        "type": "send_message",
                        "event": "wagons_update",
                        "period": self.period,
                        "wagons": "blabla",
                    },
                )
                # wait for next interval
                next_time += 1
                time.sleep(max(0, next_time - time.time()))
            time.sleep(self.period)  # TODO: Can be improved with condition variable
