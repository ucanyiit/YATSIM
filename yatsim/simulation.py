import threading
import time
from threading import Condition, Lock

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from yatsim_dashboard.models import Room


class Simulation(threading.Thread):
    def __init__(self, room: Room, period: float = 1.0):
        self.lock = Lock()
        self.cv = Condition(self.lock)
        self.room = room
        self.is_sim_alive = True
        self.is_running = False
        self.channel_layer = get_channel_layer()
        self.period = period
        super().__init__()

    # PERIODT
    def set_period(self, period):
        with self.lock:
            self.period = period

    def toggle_sim(self):
        with self.cv:
            if self.is_running:
                self.is_running = False
                return
            self.is_running = True
            self.cv.notify()

    def stop_sim(self):
        with self.cv:
            print("stop_sim aqc stop_sim")
            self.is_sim_alive = False
            self.is_running = False
            self.cv.notify()
            print("stop_sim finished")

    def run(self):
        self.is_running = True
        next_time = time.time()
        while self.is_sim_alive:
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
            with self.cv:
                print("run aqc stop_sim")
                self.cv.wait()
                next_time = time.time()
                print("run continuing")
