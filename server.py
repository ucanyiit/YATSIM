import json
from json.decoder import JSONDecodeError
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

from yatsim.room_manager import RoomManager
from yatsim.roomm import Room

room_manager = RoomManager()


class Connection(Thread):
    def __init__(self, sock):
        self.sock = sock
        self.username: str = None
        self.room: Room = None
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
            self.handle_list(request)
        elif request["command"] == "ATTACH":
            self.handle_attach(request)
        elif request["command"] == "CREATE":
            pass
        elif self.room is not None:
            if request["command"] == "DETACH":
                self.handle_detach()
            elif request["command"] == "REPLACE":
                pass
            elif request["command"] == "SWITCH":
                pass
            elif request["command"] == "START":
                pass
            elif request["command"] == "STOP":
                pass
        else:
            self.send_message("Please use a valid command type")

    def handle_login(self, request):
        if "username" not in request or "password" not in request:
            self.send_message(
                "Please add 'username' and 'password' to your 'LOGIN' request"
            )
            return
        # Check login and assign self.user if user with given credentials exists

    def handle_logout(self):
        """Forget the user."""
        if self.room is not None:
            room_manager.disconnect(self.username, self.room.identifier)
            self.room = None
        self.username = None

    def handle_detach(self):
        room_manager.disconnect(self.username, self.room.identifier)

    def handle_attach(self, request):
        room_id = request.room_id
        # Check if self.user has the room with given name or id
        self.room = room_manager.connect(self.username, self, room_id)

    def handle_list(self, request):
        # Get the list from self.user
        pass

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
