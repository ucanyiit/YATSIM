"""Simulation class is defined in this module."""

import time
from threading import Thread

from yatsim.room import Room


class Simulation(Thread):
    """Game grid class.

    Attributes:
        room: The corresponding room for the simulation.
        is_running: True if the simulation is not paused.
    """

    def __init__(self, room: Room):
        """Init simulation with given room."""
        self.room: Room = room
        self.is_running = False
        super().__init__()

    def run(self):
        """Starts running the simulation."""
        self.is_running = True
        next_time = time.time()
        while self.is_running:
            self.room.step()
            # wait for next interval
            next_time += 1
            time.sleep(max(0, next_time - time.time()))

    def start_pause(self):
        """Toggles the state of the simulation."""
        self.is_running = not self.is_running
        if self.is_running:
            self.run()
