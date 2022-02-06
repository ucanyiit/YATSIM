from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.generic.edit import FormView
from rest_framework import generics, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from .forms import (  # PlaceCellForm,; RotateCellForm,; SwitchCellForm,
    RoomCloneForm,
    RoomCreationForm,
    RoomIdForm,
    UserIdForm,
)
from .models import Cell, Room, Train, Wagon
from .serializers import (
    CreateCellSerializer,
    CreateRoomSerializer,
    DashboardData,
    DashboardRoomSerializer,
    DashboardSerializer,
    RoomData,
    RoomDataSerializer,
    RotateCellSerializer,
    UserSerializer,
)

# TODO: There are some empty control flow branches (else: pass). Let's have
# a look at them.

# pylint:disable=w0702
# TODO: Bare exceptions. What are possible exceptions and how to resolve them?
# Implement a robusts checking mechanism.


class IsRoomOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Room):
        return obj.owner == request.user


class IsRoomOwnerOrGuest(IsRoomOwner):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user in obj.guests.all() or super().has_object_permission(
            request, view, obj
        )


class IsSafeMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class DashboardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        owned_rooms = Room.objects.filter(owner=user)
        guest_rooms = Room.objects.filter(guests=user)
        data = DashboardData(user, owned_rooms, guest_rooms)
        obj = DashboardSerializer(data)
        return Response(obj.data)


class CreateRoomAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = CreateRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(owner=user)
        return Response(DashboardRoomSerializer(obj).data)


class RoomAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsRoomOwner | (IsRoomOwnerOrGuest & IsSafeMethod)]
    queryset = Room.objects.all()
    lookup_url_kwarg = "room_id"
    serializer_class = RoomDataSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # room
        trains = Train.objects.filter(room_id__exact=instance.id)
        users = User.objects.exclude(id__exact=request.user.id).exclude(
            id__in=[room.id for room in instance.guests.all()]
        )
        cell_objects = get_list_or_404(Cell, room_id__exact=instance.id)
        obj = RoomData(instance, users, cell_objects, trains)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


# TODO: ws stuff.
class RoomUserManagementAPIView(APIView):
    permission_classes = [IsRoomOwner]

    def post(self, request, room_id):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()
        new_guest = get_object_or_404(User, username=serializer.data["username"])
        room = get_object_or_404(Room, pk=room_id)
        room.guests.add(new_guest)
        room.save()
        return Response({"response": "ok"})

    def delete(self, request, room_id):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()
        user = get_object_or_404(User, username=serializer.data["username"])
        room = get_object_or_404(Room, pk=room_id)
        room.guests.remove(user)
        room.save()
        return Response({"response": "ok"})


class LeaveOrDeleteRoomAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        user = request.user
        room = get_object_or_404(Room, pk=room_id)
        if user in room.guests.all():
            room.guests.remove(user)
            room.save()
        elif user == room.owner:
            room.delete()
        else:
            raise Exception("You can not")
        return Response({"response": "ok"})


class DeleteRoomAPIView(generics.DestroyAPIView):
    permission_classes = [IsRoomOwner]
    queryset = Room.objects.all()
    lookup_url_kwarg = "room_id"


class PlaceCellAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        serializer = CreateCellSerializer(data=request.data)
        serializer.is_valid()
        cell = get_object_or_404(
            Cell, room_id=room_id, x=serializer.data["x"], y=serializer.data["y"]
        )
        room = get_object_or_404(Room, pk=room_id)

        if cell.has_wagon():
            raise Exception("Cell has a wagon on it.")

        with transaction.atomic():
            cell.delete()
            cell = Cell(room_id=room, **serializer.data)
            cell.save()

        return Response({"response": "ok"})


class SwitchCellAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        serializer = CreateCellSerializer(data=request.data)
        serializer.is_valid()
        cell = get_object_or_404(
            Cell, room_id=room_id, x=serializer.data["x"], y=serializer.data["y"]
        )
        if cell.has_wagon():
            raise Exception("The cell has a wagon on it")
        cell.switch_state()
        return Response({"response": "ok"})


class RotateCellAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        user = request.user
        room = get_object_or_404(Room, pk=room_id)
        serializer = RotateCellSerializer(data=request.data)
        serializer.is_valid()
        data = serializer.data
        direction = data["direction"]
        x = data["x"]
        y = data["y"]
        cell = get_object_or_404(Cell, room_id=room.id, x=x, y=y)
        if cell.has_wagon():
            raise Exception("The cell has a wagon on it")
        cell.rotate(str(direction))

        return Response({"response": "ok"})


class TrainAddDeleteAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        serializer = BasicCellSerializer(data=request.data)
        serializer.is_valid()
        room = get_object_or_404(Room, pk=room_id)
        t = Train(room_id=room_id, **serializer.data)
        t.save()
        return Response({"response": "ok"})

    def delete(self, request, room_id):
        t = get_object_or_404(Train, pk=request.data["train_id"])
        t.delete()
        return Response({"response": "ok"})


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
def room_view(request, room_id):
    user = request.user
    room = get_object_or_404(Room, pk=room_id)
    users = User.objects.exclude(id__exact=user.id).exclude(
        id__in=[room.id for room in room.guests.all()]
    )
    room.width_lim = room.width - 1
    room.height_lim = room.height - 1

    if user not in room.guests.all() and user != room.owner:
        raise PermissionDenied

    trains = Train.objects.filter(room_id__exact=room_id)

    running = False

    wagons = {}
    for y in range(room.height):
        for x in range(room.width):
            wagons[(y, x)] = []

    for train in trains:
        cur_wagons = Wagon.objects.filter(train=train.pk)
        for wagon in cur_wagons:
            wagons[(wagon.y, wagon.x)].append((train.type, wagon.direction))
            running = True

    cell_objects = get_list_or_404(Cell, room_id__exact=room.id)
    cells = [[" " for _ in range(room.width)] for _ in range(room.height)]
    for cell in cell_objects:
        cell_view = cell
        cell_view.type_view = cell_view.type
        if cell.state:
            cell_view.type_view += cell_view.state
        cells[cell.y][cell.x] = (cell_view, wagons.get((cell.y, cell.x)))

    stations = [c for c in cell_objects if c.type == "8"]
    statefuls = [
        (c, Cell.CELL_TYPES[int(c.type)][1])
        for c in cell_objects
        if c.type in ["3", "4", "5"]
    ]

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
            "running": running,
            "cell_types": Cell.CELL_TYPES,
            "directions": Cell.Direction.choices,
            "stateful_cells": statefuls,
        },
    )


@login_required
def clone_room(request, room_id):
    if request.method == "POST":
        user = request.user
        form = RoomCloneForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                room = get_object_or_404(Room, pk=room_id)
                new_room = Room.objects.create(
                    owner=user,
                    room_name=request.POST["room_name"],
                    height=room.height,
                    width=room.width,
                )
                new_room.save()
                cell_objects = get_list_or_404(Cell, room_id__exact=room.id)
                for cell in cell_objects:
                    new_cell = get_object_or_404(
                        Cell, room_id=new_room.id, x=cell.x, y=cell.y
                    )
                    new_cell.delete()
                    new_cell = Cell(
                        x=cell.x,
                        y=cell.y,
                        room_id=new_room,
                        type=cell.type,
                        direction=cell.direction,
                    )
                    new_cell.save()
        else:  # TODO: Empty control flow.
            pass
    return redirect("/dashboard")


# @login_
# pylint:disable=w0613


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
                        if Wagon.objects.filter(train=train):
                            raise Exception("Simulation is already started")
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
                            cell = (
                                Cell.objects.filter(room_id=room.id)
                                .filter(x=new_x)
                                .filter(y=new_y)
                            )

                            if not cell:
                                continue
                            try:
                                next_direction = cell[0].next_cell(
                                    str((int(first_wagon.direction) + 2) % 4)
                                )

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
                                first_wagon.direction = next_direction
                                first_wagon.save()
                            except:
                                pass
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
