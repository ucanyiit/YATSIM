from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from .forms import RoomCreationForm
from .models import Room

# Create your views here.


@login_required
def index(request):
    user = request.user
    owned_rooms = Room.objects.filter(owner=user)
    guest_rooms = Room.objects.filter(guests=user)
    return render(
        request,
        "dashboard/index.html",
        {"user": user, "owned_rooms": owned_rooms, "guest_rooms": guest_rooms},
    )


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


@login_required
def delete_room(request, room_id):
    user = request.user
    Room.objects.filter(id__exact=room_id).filter(owner__exact=user).delete()
    return redirect("/dashboard")
