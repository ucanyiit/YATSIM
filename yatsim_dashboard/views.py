from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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

# TODO: There are some empty control flow branches (else: pass). Let's have
# a look at them.

# pylint:disable=w0702
# TODO: Bare exceptions. What are possible exceptions and how to resolve them?
# Implement a robusts checking mechanism.


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


# TODO: add check to see whether user can access room
# TODO: some actions are owner only. We can pass a boolean is_owner context
# variable and use conditionals in the room.html to enable/disable user owner
# actions.
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


# TODO: check ownership
# Second filter does this, nvm.
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


# TODO: Can guests clone rooms?
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
            except:  # TODO: Bare except.
                pass
        else:  # TODO: Empty control flow.
            pass
    return redirect("/dashboard")


# TODO:
# - user should have access to room here.
# - boundary checking
# - refresh
# - step
# - reset


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
                # TODO: we can use an actual logger if it will help.
                print(user, room)
                # TODO: Move higher? vvv
                if room.owner == request_user:
                    room.guests.add(user)
            except:  # TODO: Bare except.
                pass
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")


# TODO:Both the owner and the guest should have permission to add/remove a guest
# from the room.
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

                # TODO: This is a cheap operation. Maybe check this before
                # DB accesses? vvv
                if room.owner == request_user:
                    room.guests.remove(user)
            except:  # TODO: Bare except.
                pass
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")
