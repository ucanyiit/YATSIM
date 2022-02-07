from threading import Lock

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from yatsim.simulation import Simulation

from .forms import RoomIdForm
from .models import Cell, Room, Train, Wagon
from .serializers import (
    CellSerializer,
    CloneRoomSerializer,
    CreateCellSerializer,
    CreateRoomSerializer,
    CreateTrainSerializer,
    DashboardData,
    DashboardRoomSerializer,
    DashboardSerializer,
    PeriodSerializer,
    RoomData,
    RoomDataSerializer,
    RotateCellSerializer,
    SimData,
    TrainSerializer,
    UserSerializer,
)

# TODO: There are some empty control flow branches (else: pass). Let's have
# a look at them.

# pylint:disable=w0702
# TODO: Bare exceptions. What are possible exceptions and how to resolve them?
# Implement a robusts checking mechanism.


sLock = Lock()
simulations = {}


def send_user_data(guests, room_id, user):
    users = User.objects.exclude(id__exact=user.id).exclude(
        id__in=[user.id for user in guests.all()]
    )
    users_data = UserSerializer(users, many=True)
    guests_data = UserSerializer(guests, many=True)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(room_id),
        {
            "type": "send_message",
            "event": "users",
            "users": users_data.data,
            "guests": guests_data.data,
        },
    )


def send_trains_data(room_id):
    trains = Train.objects.filter(room_id__exact=room_id)
    trains_data = TrainSerializer(trains, many=True)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(room_id),
        {
            "type": "send_message",
            "event": "trains",
            "trains": trains_data.data,
        },
    )


def send_cells_data(room_id):
    cells = Cell.objects.filter(room_id__exact=room_id)
    cells_data = CellSerializer(cells, many=True)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(room_id),
        {"type": "send_message", "event": "cell_change", "cells": cells_data.data},
    )


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
        alive = instance.id in simulations
        sim = SimData(
            (alive and simulations[instance.id].is_running),
            alive,
            (alive and simulations[instance.id].period),
        )
        obj = RoomData(
            instance,
            users,
            cell_objects,
            trains,
            sim,
        )

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

        send_user_data(room.guests, room.id, request.user)
        return Response({"response": "ok"})

    def delete(self, request, room_id):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()
        user = get_object_or_404(User, username=serializer.data["username"])
        room = get_object_or_404(Room, pk=room_id)
        room.guests.remove(user)
        room.save()

        send_user_data(room.guests, room.id, request.user)
        return Response({"response": "ok"})


class LeaveOrDeleteRoomAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        user = request.user
        room = get_object_or_404(Room, pk=room_id)
        if user in room.guests.all():
            room.guests.remove(user)
            room.save()
            send_user_data(room.guests, room.id, request.user)
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

        send_cells_data(room_id)
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

        send_cells_data(room_id)
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

        send_cells_data(room_id)
        return Response({"response": "ok"})


class TrainAddDeleteAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        serializer = CreateTrainSerializer(data=request.data)
        serializer.is_valid()
        data = serializer.data
        room = get_object_or_404(Room, pk=room_id)
        cell = get_object_or_404(
            Cell,
            room_id=room,
            x=data["source"]["x"],
            y=data["source"]["y"],
        )
        t = Train(
            room_id=room,
            source=cell,
            type=data["type"],
            length=data["length"],
        )
        t.save()
        send_trains_data(room_id)
        return Response({"response": "ok"})

    def delete(self, request, room_id):
        t = get_object_or_404(Train, pk=request.data["train_id"])
        t.delete()
        send_trains_data(room_id)
        return Response({"response": "ok"})


class CloneRoomAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        user = request.user
        serializer = CloneRoomSerializer(data=request.data)
        serializer.is_valid()
        data = serializer.data
        room = get_object_or_404(Room, pk=room_id)
        with transaction.atomic():
            new_room = Room.objects.create(
                owner=user,
                room_name=data["room_name"],
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
        return Response({"response": "ok"})


# pylint:disable=w0613


class StartSimulationAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        trains = get_list_or_404(Train, room_id=room.id)
        serializer = PeriodSerializer(data=request.data)
        serializer.is_valid()
        with sLock:
            if simulations.get(room_id) is not None:
                raise Exception("Simulation has already started")
            with transaction.atomic():
                for train in trains:
                    Wagon.objects.filter(train__in=trains).delete()
                    source = train.source
                    wagon = Wagon(
                        x=source.x,
                        y=source.y,
                        direction=source.direction,
                        train=train,
                    )
                    wagon.save()
                t = Simulation(room, serializer.data["period"])
                simulations[room.id] = t
                t.start()

        return Response({"response": "ok"})


class StopSimulationAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        with sLock:
            if simulations.get(room_id) is None:
                raise Exception("No simulations running.")
            simulations[room_id].stop_sim()
            simulations.pop(room_id)
        return Response({"response": "ok"})


class ToggleSimulationAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        with sLock:
            if simulations.get(room_id) is None:
                raise Exception("No simulations running.")
            simulations[room_id].toggle_sim()
        return Response({"response": "ok"})


class SimulationPeriodAPIView(APIView):
    permission_classes = [IsRoomOwnerOrGuest]

    def post(self, request, room_id):
        serializer = PeriodSerializer(data=request.data)
        serializer.is_valid()
        with sLock:
            if simulations.get(room_id) is None:
                raise Exception("No simulations running.")
            simulations[room_id].set_period(serializer.data["period"])
        return Response({"response": "ok"})


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
