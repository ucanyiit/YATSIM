import json
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


class Connection(Thread):
    def __init__(self, sock):
        self.sock = sock
        self.user = None
        self.room = None
        super().__init__()

    def run(self):
        self.send_message("Please enter a username and password.")

        req = self.sock.recv(1024)
        while req and req != "":
            try:
                req_json = json.loads(req.decode())

                if "command" not in req_json:
                    self.send_message("Send your request with a command")
                elif self.user is None:
                    if req_json["command"] == "LOGIN":
                        self.handle_login(req_json)
                    else:
                        self.send_message("Log in before sending different requests.")
                elif req_json["command"] == "LOGOUT":
                    self.handle_logout()
                elif req_json["command"] == "LIST":
                    self.handle_list(req_json)
                elif req_json["command"] == "ATTACH":
                    self.handle_attach(req_json)
                else:
                    self.send_message("Please use a valid command type")

            except:
                self.send_message("Send your request in JSON format")

            req = self.sock.recv(1024)

        print(self.sock.getpeername(), " closing")

    def handle_login(self, request):
        if "username" not in request or "password" not in request:
            self.send_message(
                "Please add 'username' and 'password' to your 'LOGIN' request"
            )
            return
        # Check login and assign self.user if user with given credentials exists

    def handle_logout(self):
        """Forget the user."""
        self.user = None

    def handle_attach(self, request):
        # Check if self.user has the room with given name or id
        # If it has, then self.room = (that room)
        pass

    def handle_list(self, request):
        # Get the list from self.user
        pass

    def send_message(self, message):
        msg = {"type": "MSG", "message": message}
        self.sock.send(json.dumps(msg).encode())


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
