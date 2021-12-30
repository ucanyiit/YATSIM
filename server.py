import json
from json.decoder import JSONDecodeError
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

from yatsim.cell.cell_element import Direction
from yatsim.room import Room
from yatsim.room_manager import RoomManager
from yatsim.user import UserManager

room_manager = RoomManager()
user_manager = UserManager()


class Connection(Thread):
    def __init__(self, sock):
        self.sock = sock
        self.username: str = None
        self.room: Room = None
        self.user_id: int = 0
        super().__init__()

    def run(self):
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
        if "username" not in request or "password" not in request:
            self.send_message(
                "Please add 'username' and 'password' to your 'LOGIN' request"
            )
            return
        if user_manager.login(request["username"], request["password"]):
            self.username = request["username"]
            self.send_message("OK")
        else:
            self.send_message("Wrong password.")

    def handle_logout(self):
        """Forget the user."""
        if self.room is not None:
            room_manager.disconnect(self.username, self.room.room_name)
            self.room = None
        self.username = None
        self.send_message("OK")

    def handle_detach(self):
        room_manager.disconnect(self.username, self.room.room_name)
        self.room = None
        self.send_message("OK")

    def handle_attach(self, request):
        if user_manager.check_room_id(self.username, request["room_id"]):
            self.room = room_manager.connect(self.username, self, request["room_id"])

    def handle_list(self):
        l = user_manager.get_game_grid_list(self.username)
        msg = {"type": "MSG", "message": l}
        self.sock.send(json.dumps(msg).encode())

    def handle_create(self, request):
        room_id = room_manager.create_game_grid(request["height"], request["width"])
        self.send_message(f"New room created with identifier: {room_id}")

    def send_message(self, message):
        msg = {"type": "MSG", "message": message}
        self.sock.send(json.dumps(msg).encode())

    def send_update(self, update):
        self.sock.send(json.dumps(update).encode())


if __name__ == "__main__":
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("", 20441))
    s.listen()
    try:
        while True:
            ns, peer = s.accept()
            print(peer, "connected")
            # Create a Connection (thread) with new socket
            t = Connection(ns)
            t.start()
    finally:
        s.close()
