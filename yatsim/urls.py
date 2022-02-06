"""yatsim URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from yatsim_dashboard import views

urlpatterns = [
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="auth/logout.html"),
        name="logout",
    ),
    path("admin/", admin.site.urls),
    path("dashboard/", views.DashboardAPIView.as_view(), name="dashboard"),
    path(
        "create_room/",
        views.CreateRoomAPIView.as_view(),
        name="create_room_new",
    ),
    path("room/<int:room_id>", views.RoomAPIView.as_view(), name="room_view_delete"),
    path(
        "room/<int:room_id>/user/",
        views.RoomUserManagementAPIView.as_view(),
        name="guest add/delete",
    ),
    path(
        "room/<int:room_id>/leave/",
        views.LeaveOrDeleteRoomAPIView.as_view(),
        name="leave room",
    ),
    path(
        "room/<int:room_id>/place/",
        views.PlaceCellAPIView.as_view(),
        name="place_cell",
    ),
    path(
        "room/<int:room_id>/switch/",
        views.SwitchCellAPIView.as_view(),
        name="switch_cell",
    ),
    path(
        "room/<int:room_id>/rotate/",
        views.RotateCellAPIView.as_view(),
        name="rotate_cell",
    ),
    path(
        "room/<int:room_id>/train/",
        views.TrainAddDeleteAPIView.as_view(),
        name="train add/remove",
    ),
    path(
        "room/start/<int:room_id>/",
        views.start_simulation,
        name="start",
    ),
    path(
        "room/stop/<int:room_id>/",
        views.stop_simulation,
        name="stop",
    ),
    path(
        "room/run/<int:room_id>/",
        views.run_simulation,
        name="run",
    ),
    path(
        "room/<int:room_id>/clone/", views.CloneRoomAPIView.as_view(), name="clone_room"
    ),
]
