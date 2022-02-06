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
from django.contrib.auth.decorators import login_required
from django.urls import path

from yatsim_dashboard import views
from yatsim_user import views as user_views

urlpatterns = [
    # path(
    #     "login/",
    #     auth_views.LoginView.as_view(
    #         template_name="auth/login.html", redirect_authenticated_user=True
    #     ),
    #     name="login",
    # ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="auth/logout.html"),
        name="logout",
    ),
    path("admin/", admin.site.urls),
    path("dashboard/", views.DashboardAPIView.as_view(), name="dashboard"),
    path(
        "create_room/",
        login_required(views.CreateRoomView.as_view()),
        name="create_room",
    ),
    # path("room/<int:room_id>/", views.index, name="room_page"),
    path("room/delete/<int:room_id>/", views.delete_room, name="delete_room"),
    path("room/clone/<int:room_id>/", views.clone_room, name="clone_room"),
    path("room/<int:room_id>", views.room_view, name="room"),
    path("room/add/<int:room_id>/", views.add_user_to_room, name="add_user_to_room"),
    path(
        "room/remove/<int:room_id>/",
        views.remove_user_from_room,
        name="remove_user_from_room",
    ),
    path(
        "room/leave/<int:room_id>/",
        views.leave_from_room,
        name="leave_from_room",
    ),
    path(
        "room/place/<int:room_id>/",
        views.place_cell,
        name="place_cell",
    ),
    path(
        "room/switch/<int:room_id>/",
        views.switch_cell,
        name="switch_cell",
    ),
    path(
        "room/rotate/<int:room_id>/",
        views.rotate_cell,
        name="rotate_cell",
    ),
    path(
        "room/add_train/<int:room_id>/",
        views.add_train,
        name="add_train",
    ),
    path(
        "room/remove_train/<int:room_id>/",
        views.remove_train,
        name="remove_train",
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
    path("api/auth/login/", user_views.LoginAPIView.as_view()),
]
