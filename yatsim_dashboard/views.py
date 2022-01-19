from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.generic.edit import FormView

from .forms import (  # PlaceCellForm,; RotateCellForm,; SwitchCellForm,
    RoomCloneForm,
    RoomCreationForm,
    RoomIdForm,
    UserIdForm,
)
from .models import Cell, Room, Train, Wagon

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

    trains = Train.objects.filter(room_id__exact=room_id)

    wagons = {}
    for train in trains:
        cur_wagons = Wagon.objects.filter(train=train.pk)
        for wagon in cur_wagons:
            wagons[(wagon.y, wagon.x)] = (train.type, wagon.direction)

    cell_objects = get_list_or_404(Cell, room_id__exact=room.id)
    cells = [[" " for _ in range(room.width)] for _ in range(room.height)]
    for cell in cell_objects:
        cells[cell.y][cell.x] = (cell, wagons.get((cell.y, cell.x)))
        if wagons.get((cell.y, cell.x)):
            print(wagons.get((cell.y, cell.x)))

    stations = [c for c in cell_objects if c.type == "8"]

    return render(
        request,
        "dashboard/room.html",
        {
            "user": user,
            "room": room,
            "users": users,
            "is_owner": room.owner == user,
            "cells": cells,
            "stations": stations,
            "trains": trains,
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
                if int(cell_type) > 8 or int(cell_type) < 0:
                    raise Exception("Cell type is not defined.")
                cell = get_object_or_404(Cell, room_id=room.id, x=x, y=y)
                with transaction.atomic():
                    cell.delete()
                    cell = Cell(x=x, y=y, room_id=room, type=cell_type)
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
                if int(direction) > 3 or int(direction) < 0:
                    raise Exception("Direction is not defined.")
                cell = get_object_or_404(Cell, room_id=room.id, x=x, y=y)
                cell.rotate(str(direction))
            else:
                raise PermissionDenied
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")


# pylint:disable=w0613


@login_required
def add_train(request, room_id):
    user = request.user
    room = get_object_or_404(Room, pk=room_id)
    if request.method == "POST":
        if user in room.guests.all() or user == room.owner:
            data = request.POST
            if data["train_type"] not in ["0", "1"]:
                raise Exception("Train type should be '0' or '1'")
            station = get_object_or_404(Cell, pk=data["station_id"])
            if station.type != "8":
                raise Exception("Not a station :( don't be cheeky.")
            exists = Train.objects.filter(source=station)
            if exists:
                raise Exception(
                    "Station is full. Remove existing train from the station."
                )
            train = Train(
                room_id=room,
                type=data["train_type"],
                length=data["train_length"],
                source=station,
            )
            train.save()
        else:
            raise PermissionDenied
    return redirect(f"/room/{room_id}")


@login_required
def remove_train(request, room_id):
    user = request.user
    room = get_object_or_404(Room, pk=room_id)
    if request.method == "POST":
        if user in room.guests.all() or user == room.owner:
            train_id = request.POST["train_id"]
            train = get_object_or_404(Train, pk=train_id)
            train.delete()
        else:
            raise PermissionDenied
    return redirect(f"/room/{room_id}")


@login_required
def start_simulation(request, room_id):
    if request.method == "POST":
        user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        if room_form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            if user in room.guests.all() or user == room.owner:
                trains = get_list_or_404(Train, room_id=room.id)
                with transaction.atomic():
                    for train in trains:
                        source = train.source
                        wagon = Wagon(
                            x=source.x,
                            y=source.y,
                            direction=source.direction,
                            train=train,
                        )
                        wagon.save()
            else:
                raise PermissionDenied
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")


@login_required
def stop_simulation(request, room_id):
    if request.method == "POST":
        user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        if room_form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            if user in room.guests.all() or user == room.owner:
                trains = Train.objects.filter(room_id=room.id)
                with transaction.atomic():
                    for train in trains:
                        Wagon.objects.filter(train=train.pk).delete()
            else:
                raise PermissionDenied
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")


@login_required
def run_simulation(request, room_id):
    if request.method == "POST":
        user = request.user
        room_form = RoomIdForm(request.POST, request.FILES)
        if room_form.is_valid():
            room = get_object_or_404(Room, pk=room_id)
            if user in room.guests.all() or user == room.owner:
                step_count = request.POST["step_count"]
                with transaction.atomic():
                    for _ in range(0, int(step_count)):
                        trains = Train.objects.filter(room_id=room.id)
                        for train in trains:
                            wagons = Wagon.objects.filter(train=train.pk)

                            first_wagon = wagons[0]
                            new_x, new_y = get_new_coord(
                                first_wagon.x, first_wagon.y, first_wagon.direction
                            )
                            for wagon in wagons:
                                print(
                                    wagon.sequence_id, wagon.x, wagon.y, wagon.direction
                                )
                            print(
                                first_wagon.x,
                                first_wagon.y,
                                first_wagon.direction,
                                new_x,
                                new_y,
                            )
                            cell = (
                                Cell.objects.filter(room_id=room.id)
                                .filter(x=new_x)
                                .filter(y=new_y)
                            )

                            if not cell:
                                break

                            for i in range(len(wagons) - 1, 0, -1):
                                wagon = wagons[i]
                                front_wagon = wagons[i - 1]
                                wagon.x = front_wagon.x
                                wagon.y = front_wagon.y
                                wagon.direction = front_wagon.direction
                                wagon.save()

                            if train.length > len(wagons):
                                source = train.source
                                wagon = Wagon(
                                    x=source.x,
                                    y=source.y,
                                    direction=source.direction,
                                    train=train,
                                )
                                wagon.save()

                            first_wagon.x = new_x
                            first_wagon.y = new_y
                            first_wagon.direction = cell[0].next_cell(
                                str((int(first_wagon.direction) + 2) % 4)
                            )
                            first_wagon.save()
                            print(first_wagon)

                            print(wagons)
            else:
                raise PermissionDenied
        else:  # TODO: Empty control flow.
            pass
    return redirect(f"/room/{room_id}")


def get_new_coord(x, y, direction):
    if direction == "0":
        return (x, y - 1)
    if direction == "1":
        return (x + 1, y)
    if direction == "2":
        return (x, y + 1)
    if direction == "3":
        return (x - 1, y)
    raise Exception("Direction is not defined")
