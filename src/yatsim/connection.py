"""Connection class is defined in this module"""

import json
from json.decoder import JSONDecodeError
from socket import socket
from threading import Thread

from yatsim import room as r
from yatsim import room_manager as rm
from yatsim.cell.cell_element import Direction
from yatsim.user import UserManager


class Connection(Thread):
    """The class that handles connection & requests of a client.

    Attributes:
        room_manager: The room manager class that Connection uses to handle
        room related requests.
        user_manager: The user manager class that Connection uses to handle
        user related requests.
        sock: Socket to communicate with the user.
    """

    def __init__(
        self,
        sock: socket,
        room_manager: rm.RoomManager,
        user_manager: UserManager,
    ):
        """Inits connection with socket, usermanager and room manager."""
        self.user_manager = user_manager
        self.room_manager = room_manager
        self.sock = sock
        self.username: str = None
        self.room: r.Room = None
        self.user_id: int = 0
        super().__init__()

    def run(self):
        """Starts connection to handle incoming requests."""
        self.send_message("Please enter a username and password.")

        req = self.sock.recv(1024)
        while req and req != "":
            try:
                self.handle_request(json.loads(req.decode()))
            except JSONDecodeError:
                self.send_message("Send your request in JSON format")

            req = self.sock.recv(1024)

        print(self.sock.getpeername(), " closing")

    def handle_request(self, request):
        """Handle a single request thats incoming from a client."""
        if "command" not in request:
            self.send_message("Send your request with a command")
        elif self.username is None:
            if request["command"] == "LOGIN":
                self.handle_login(request)
            else:
                self.send_message("Log in before sending different requests.")
        elif request["command"] == "LOGOUT":
            self.handle_logout()
        elif request["command"] == "LIST":
            self.handle_list()
        elif request["command"] == "ATTACH":
            self.handle_attach(request)
        elif request["command"] == "CREATE":
            self.handle_create(request)
        elif self.room is not None:
            if request["command"] == "DETACH":
                self.handle_detach()
            elif request["command"] == "PLACE":
                self.room.handle_place(request["x"], request["y"], request["cell_type"])
            elif request["command"] == "SWITCH":
                self.room.handle_switch(request["x"], request["y"])
            elif request["command"] == "ROTATE":
                self.room.handle_rotate(
                    request["x"], request["y"], Direction(request["direction"])
                )
            elif request["command"] == "START":
                self.room.handle_start_simulation()
            elif request["command"] == "STOP":
                self.room.handle_stop_simulation()
            elif request["command"] == "TOGGLE":
                self.room.handle_toggle_simulation()
        else:
            self.send_message("Please use a valid command type")

    def handle_login(self, request):
        """Handles login request, checks the username and passowrd."""
        if "username" not in request or "password" not in request:
            self.send_message(
                "Please add 'username' and 'password' to your 'LOGIN' request"
            )
            return
        if self.user_manager.login(request["username"], request["password"]):
            self.username = request["username"]
            self.send_update({"type": "LOGIN", "username": self.username})
        else:
            self.send_message("Wrong password.")

    def handle_logout(self):
        """Handles logout request, forgets the user."""
        if self.room is not None:
            self.room_manager.disconnect(self.username, self.room.room_name)
            self.room = None
        self.username = None
        self.send_update({"type": "LOGOUT"})

    def handle_detach(self):
        """Handles detach request, detachs user if they are connected to a room."""
        self.room_manager.disconnect(self.username, self.room.room_name)
        self.room = None
        self.send_message("OK")

    def handle_attach(self, request):
        """Handles attach request, connects the user to the requested room."""
        if self.user_manager.check_room_id(self.username, request["room_id"]):
            self.room = self.room_manager.connect(
                self.username, self, request["room_id"]
            )

    def handle_list(self):
        """Handles list request, lists all of the available rooms to the user."""
        l = self.user_manager.get_game_grid_list(self.username)
        msg = {"type": "MSG", "message": l}
        self.sock.send(json.dumps(msg).encode())

    def handle_create(self, request):
        """Handles create request, creates a game grid with requested w and h."""
        room_id = self.room_manager.create_game_grid(
            request["height"], request["width"]
        )
        self.send_message(f"New room created with identifier: {room_id}")

    def send_message(self, message):
        """Sends a simple message to the user."""
        msg = {"type": "MSG", "message": message}
        self.sock.send(json.dumps(msg).encode())

    def send_update(self, update):
        """Sends a raw message to the user."""
        self.sock.send(json.dumps(update).encode())
