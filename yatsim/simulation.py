import threading
import time
from threading import Condition, Lock

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction

from yatsim_dashboard.communication import send_trains_data
from yatsim_dashboard.models import Cell, Room, Train, Wagon


def get_new_coord(x, y, direction):
    if direction == "0":
        return (x, y - 1)
    if direction == "1":
        return (x + 1, y)
    if direction == "2":
        return (x, y + 1)
    if direction == "3":
        return (x - 1, y)
    raise Exception("Direction is not defined")


class Simulation(threading.Thread):
    def __init__(self, room: Room, period: float = 1.0):
        self.lock = Lock()
        self.cv = Condition(self.lock)
        self.room = room
        self.is_sim_alive = True
        self.is_running = True
        self.channel_layer = get_channel_layer()
        self.period = period
        send_trains_data(self.room.id)
        self._send_update()
        super().__init__()

    def _send_update(self):
        async_to_sync(self.channel_layer.group_send)(
            str(self.room.id),
            {
                "type": "send_message",
                "event": "sim_update",
                "sim": {
                    "alive": self.is_sim_alive,
                    "running": self.is_running,
                    "period": self.period,
                },
            },
        )

    def set_period(self, period):
        with self.lock:
            self.period = period
            self._send_update()

    def toggle_sim(self):
        with self.cv:
            if self.is_running:
                self.is_running = False
            else:
                self.is_running = True
                self.cv.notify()

            self._send_update()

    def stop_sim(self):
        with self.cv:
            self.is_sim_alive = False
            self.is_running = False
            self.cv.notify()
            self._send_update()

    def run(self):
        self.is_running = True
        next_time = time.time()
        while self.is_sim_alive:
            next_time += self.period
            time.sleep(max(0, next_time - time.time()))
            while self.is_running:
                # update wagons
                # wait for next interval
                self.simulation_step()
                send_trains_data(self.room.id)
                next_time += self.period
                time.sleep(max(0, next_time - time.time()))

            with self.cv:
                print("run aqc stop_sim")
                self.cv.wait()
                next_time = time.time()
                print("run continuing")

    def simulation_step(self):
        with transaction.atomic():
            trains = Train.objects.filter(room_id=self.room.id)
            for train in trains:
                wagons = Wagon.objects.filter(train=train.pk)
                if len(wagons) == 0:
                    continue
                first_wagon = wagons[0]
                new_x, new_y = get_new_coord(
                    first_wagon.x, first_wagon.y, first_wagon.direction
                )
                cell = (
                    Cell.objects.filter(room_id=self.room.id)
                    .filter(x=new_x)
                    .filter(y=new_y)
                )

                if not cell:
                    continue
                try:
                    next_direction = cell[0].next_cell(
                        str((int(first_wagon.direction) + 2) % 4)
                    )

                    for i in range(len(wagons) - 1, 0, -1):
                        wagon = wagons[i]
                        front_wagon = wagons[i - 1]
                        wagon.x = front_wagon.x
                        wagon.y = front_wagon.y
                        wagon.direction = front_wagon.direction
                        wagon.save()

                    if train.length > len(wagons):
                        source = train.source
                        wagon = Wagon(
                            x=source.x,
                            y=source.y,
                            direction=source.direction,
                            train=train,
                        )
                        wagon.save()

                    first_wagon.x = new_x
                    first_wagon.y = new_y
                    first_wagon.direction = next_direction
                    first_wagon.save()
                except:
                    pass
