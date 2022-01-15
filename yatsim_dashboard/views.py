from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from .forms import (
    RoomCloneForm,
    RoomCreationForm,
    RoomDeletionForm,
    RoomIdForm,
    UserIdForm,
)
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
        {
            "user": user,
            "owned_rooms": owned_rooms,
            "guest_rooms": guest_rooms,
        },
    )


@login_required
def room_view(request, room_id):
    user = request.user
    room = Room.objects.get(id=room_id)
    users = User.objects.exclude(id__exact=user.id).exclude(
        id__in=[room.id for room in room.guests.all()]
    )
    return render(
        request,
        "dashboard/room.html",
        {
            "user": user,
            "room": room,
            "users": users,
        },
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
    if request.method == "POST":
        user = request.user
        form = RoomDeletionForm(request.POST, request.FILES)
        if form.is_valid():
            Room.objects.filter(id__exact=room_id).filter(owner__exact=user).delete()
        else:
            pass
    return redirect("/dashboard")


@login_required
def clone_room(request, room_id):
    if request.method == "POST":
        user = request.user
        form = RoomCloneForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                room = Room.objects.get(id=room_id)
                if room.owner == user:
                    new_room = Room.objects.create(
                        owner=user,
                        room_name=request.POST["room_name"],
                        height=room.height,
                        width=room.width,
                    )
                    new_room.save()
            except:
                pass
        else:
            pass
    return redirect("/dashboard")


@login_required
def place_cell(request):
    pass


@login_required
def switch_cell(request):
    pass


@login_required
def rotate_cell(request):
    pass


@login_required
def add_user_to_room(request, room_id):
    if request.method == "POST":
        request_user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        user_form = UserIdForm(request.POST, request.FILES)
        if room_form.is_valid() and user_form.is_valid():
            try:
                room = Room.objects.get(id=room_id)
                user = User.objects.get(id=request.POST["user_id"])
                print(user, room)
                if room.owner == request_user:
                    room.guests.add(user)
            except:
                pass
        else:
            pass
    return redirect(f"/room/{room_id}")


@login_required
def remove_user_from_room(request, room_id):
    if request.method == "POST":
        request_user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        user_form = UserIdForm(request.POST, request.FILES)
        if room_form.is_valid() and user_form.is_valid():
            try:
                room = Room.objects.get(id=room_id)
                user = User.objects.get(id=request.POST["user_id"])
                if room.owner == request_user:
                    room.guests.remove(user)
            except:
                pass
        else:
            pass
    return redirect(f"/room/{room_id}")
