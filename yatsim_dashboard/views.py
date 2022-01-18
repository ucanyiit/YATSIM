from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.generic.edit import FormView

from .forms import (  # PlaceCellForm,; RotateCellForm,; SwitchCellForm,
    RoomCloneForm,
    RoomCreationForm,
    RoomIdForm,
    UserIdForm,
)
from .models import Cell, Room

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


@login_required
def room_view(request, room_id):
    user = request.user
    room = get_object_or_404(Room, pk=room_id)
    users = User.objects.exclude(id__exact=user.id).exclude(
        id__in=[room.id for room in room.guests.all()]
    )

    if user not in room.guests.all() and user != room.owner:
        raise PermissionDenied

    cell_objects = get_list_or_404(Cell, room_id__exact=room.id)
    cells = [[" " for _ in range(room.width)] for _ in range(room.height)]
    for cell in cell_objects:
        cells[cell.y][cell.x] = cell

    return render(
        request,
        "dashboard/room.html",
        {
            "user": user,
            "room": room,
            "users": users,
            "is_owner": room.owner == user,
            "cells": cells,
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
        form = RoomIdForm(request.POST, request.FILES)
        if form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            if user != room.owner:
                raise PermissionDenied
            else:
                room.delete()
        else:  # TODO: Empty control flow.
            pass
    return redirect("/dashboard")


@login_required
def clone_room(request, room_id):
    if request.method == "POST":
        user = request.user
        form = RoomCloneForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                room = get_object_or_404(Room, pk=room_id)
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


@login_required
def add_user_to_room(request, room_id):
    if request.method == "POST":
        request_user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        user_form = UserIdForm(request.POST, request.FILES)
        if room_form.is_valid() and user_form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            user = get_object_or_404(User, pk=request.POST["user_id"])
            if room.owner == request_user:
                room.guests.add(user)
            else:
                raise PermissionDenied
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")


@login_required
def remove_user_from_room(request, room_id):
    if request.method == "POST":
        request_user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        user_form = UserIdForm(request.POST, request.FILES)
        if room_form.is_valid() and user_form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            user = get_object_or_404(User, pk=request.POST["user_id"])
            if room.owner == request_user:
                room.guests.remove(user)
            else:
                raise PermissionDenied
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")


@login_required
def leave_from_room(request, room_id):
    if request.method == "POST":
        user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        if room_form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            if room.owner != user:
                room.guests.remove(user)
            else:
                raise PermissionDenied
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
def place_cell(request, room_id):
    if request.method == "POST":
        user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        # cell_form = PlaceCellForm(request.POST, request.FILES)
        if room_form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            if user in room.guests.all() or user == room.owner:
                data = request.POST
                x = data["x"]
                y = data["y"]
                cell_type = data["type"]
                if cell_type > "8" or cell_type < "0":
                    raise Exception("Cell type is not defined.")
                cell = get_object_or_404(Cell, room_id=room.id, x=x, y=y)
                cell.type = cell_type
                cell.save()
            else:
                raise PermissionDenied
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")


@login_required
def switch_cell(request, room_id):
    if request.method == "POST":
        user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        # cell_form = SwitchCellForm(request.POST, request.FILES)
        if room_form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            if user in room.guests.all() or user == room.owner:
                data = request.POST
                x = data["x"]
                y = data["y"]
                cell = get_object_or_404(Cell, room_id=room.id, x=x, y=y)
                cell.switch_state()
            else:
                raise PermissionDenied
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")


@login_required
def rotate_cell(request, room_id):
    if request.method == "POST":
        user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        # cell_form = RotateCellForm(request.POST, request.FILES)
        if room_form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            if user in room.guests.all() or user == room.owner:
                data = request.POST
                x = data["x"]
                y = data["y"]
                direction = data["direction"]
                if direction < "0" or direction > "3":
                    raise Exception("Direction is not defined.")
                cell = get_object_or_404(Cell, room_id=room.id, x=x, y=y)
                cell.rotate(str(direction))
            else:
                raise PermissionDenied
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")
