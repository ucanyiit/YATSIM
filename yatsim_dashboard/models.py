"""Models displayed in main page."""

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=32, blank=False, null=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_rooms",
        related_query_name="owned_room",
    )

    height = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(2), MaxValueValidator(16)],
    )

    width = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(2), MaxValueValidator(16)],
    )

    guests = models.ManyToManyField(
        User,
        related_name="accessible_rooms",
        related_query_name="accessible_room",
        blank=True,
    )

    active_players = models.PositiveSmallIntegerField(
        blank=False, null=False, default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Room: ({self.pk}) - {self.owner.username}/{self.room_name}>"


# TODO: save()
# TODO: __str__()
class Cell(models.Model):

    CELL_TYPES = [
        ("0", "Blank"),
        ("1", "Straight"),
        ("2", "Curved"),
        ("3", "Y Junction"),
        ("4", "Y Junction Mirrored"),
        ("5", "X Junction"),
        ("6", "Cross Roads"),
        ("7", "Cross Bridge"),
        ("8", "Station"),
    ]

    class Direction(models.TextChoices):
        NORTH = ("0", "NORTH")
        EAST = ("1", "EAST")
        SOUTH = ("2", "SOUTH")
        WEST = ("3", "WEST")

    class State(models.TextChoices):
        CCW = ("0", "Counter Clockwise Routing")
        STRAIGHT = ("1", "Straight Routing")
        CW = ("2", "Clockwise Routing")

    room_id = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="cells", related_query_name="cell"
    )
    x = models.PositiveSmallIntegerField(blank=False, null=False)
    y = models.PositiveSmallIntegerField(blank=False, null=False)
    type = models.CharField(max_length=1, choices=CELL_TYPES, blank=False, null=False)
    direction = models.CharField(
        max_length=1, choices=Direction.choices, blank=False, null=False
    )

    state = models.CharField(max_length=1, choices=State.choices, null=True)

    class Meta:
        unique_together = (("room_id", "x", "y"),)

    def rotate(self, direction: Direction) -> None:
        self.direction = direction
        self.save()

    def switch_state(self) -> None:
        if self.type not in ["3", "4", "5"]:
            raise Exception("Not stateful cell: {self.x}, {self.y}")

        if self.type == "3":
            if self.state == "1":
                self.state = "2"
            elif self.state == "2":
                self.state = "1"

        elif self.type == "4":
            if self.state == "1":
                self.state = "0"
            elif self.state == "0":
                self.state = "1"

        elif self.type == "5":
            if self.state == "0":
                self.state = "1"
            elif self.state == "1":
                self.state = "2"
            else:  # self.state == "2":
                self.state = "0"
        self.save()

    def next_cell(self, entry: str) -> str:

        if self.type == "0":
            raise Exception(f"0 cell {self.x}, {self.y}, {entry}")

        if self.type in ["1", "8"]:
            opposite = str((int(self.direction) + 2) % 4)
            if entry == self.direction:
                return opposite
            if entry == opposite:
                return self.direction
            raise Exception(f"1 cell {self.x}, {self.y}, {entry}")
        if self.type == "2":
            opposite = str((int(self.direction) + 1) % 4)
            if entry == self.direction:
                return opposite
            if entry == opposite:
                return self.direction
            raise Exception(f"2 cell {self.x}, {self.y}, {entry}")

        if self.type == "3":
            if entry == str((int(self.direction) + 3) % 4):
                raise Exception(f"3 cell {self.x}, {self.y}, {entry}")

            if entry != self.direction:
                return self.direction

            return str((int(self.direction) + (2 if self.state == "1" else 1)) % 4)

        if self.type == "4":
            if entry == str((int(self.direction) + 1) % 4):
                raise Exception(f"4 cell {self.x}, {self.y}, {entry}")

            if entry != self.direction:
                return self.direction

            return str((int(self.direction) + (2 if self.state == "1" else 3)) % 4)

        if self.type == "5":
            if entry != self.direction:
                return self.direction
            return str((int(self.direction) + 1 + int(entry)) % 4)

        if self.type in ["6", "7"]:
            return str((int(self.direction) + 2) % 4)

        raise Exception("Impossible control flow")
