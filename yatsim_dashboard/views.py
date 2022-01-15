from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import RoomCreationForm
from .models import Room

# Create your views here.


@login_required
def index(request):
    user = request.user
    rooms = Room.objects.filter(owner__exact=user)
    return render(request, "dashboard/index.html", {"user": user, "rooms": rooms})


class CreateRoomView(FormView):
    template_name = "dashboard/create_room.html"
    form_class = RoomCreationForm
    success_url = "/dashboard"

    def form_valid(self, form):
        user = self.request.user
        data = self.request.POST
        room_name = data["room_name"]
        height = data["height"]
        width = data["width"]
        new_room = Room.objects.create(
            owner=user, room_name=room_name, height=height, width=width
        )
        new_room.save()
        return super().form_valid(form)
