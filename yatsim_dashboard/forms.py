from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Room


class RoomCreationForm(ModelForm):
    class Meta:
        model = Room
        fields = ["room_name", "height", "width"]


class RoomCloneForm(ModelForm):
    class Meta:
        model = Room
        fields = ["id", "room_name"]


class RoomIdForm(ModelForm):
    class Meta:
        model = Room
        fields = ["id"]


class UserIdForm(ModelForm):
    class Meta:
        model = User
        fields = ["id"]


class PlaceCellForm(ModelForm):
    class Meta:
        model = ...
        fields = ["x", "y", "type"]


class SwitchCellForm(ModelForm):
    class Meta:
        model = ...
        fields = ["x", "y"]


class RotateCellForm(ModelForm):
    class Meta:
        model = ...
        fields = ["x", "y", "direction"]
