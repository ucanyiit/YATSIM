"""Models displayed in main page."""

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


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
