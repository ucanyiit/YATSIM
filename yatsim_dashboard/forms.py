from django.forms import ModelForm

from .models import Room


class RoomCreationForm(ModelForm):
    class Meta:
        model = Room
        fields = ["room_name", "height", "width"]

class RoomDeletionForm(ModelForm):
    class Meta:
        model = Room
        fields = ["id"]
