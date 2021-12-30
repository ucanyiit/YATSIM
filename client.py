import json
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

from visualizer2 import Visualizer

messages = [
    '{ "command": "LOGIN", "username": "12345", "password": "123"}',
    '{ "command": "LOGOUT }',
]


class Client:
    def __init__(self, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(("127.0.0.1", port))
        self.username = ""
        self.visualizer = None

        incoming_messages = Thread(target=self.incoming_message_handler, args=(sock,))
        incoming_messages.start()

        while True:
            inp = input()
            if inp == "exit":
                break
            sock.send(inp.encode())

        sock.close()
        incoming_messages.wait()

    def incoming_message_handler(self, sock):
        while True:
            reply = sock.recv(1024)
            msg = json.loads(reply.decode())
            self.handle_nessage(msg)

    def handle_nessage(self, msg):
        if msg["type"] == "MSG":
            print(msg["message"])
        elif msg["type"] == "LOGIN":
            self.username = msg["username"]
            print(f"Logged in with {self.username}.")
        elif msg["type"] == "LOGOUT":
            self.username = ""
            print("Logged out.")
        elif msg["type"] == "VIEW":
            self.visualizer = Visualizer(msg["height"], msg["width"], msg["view"])
        elif msg["type"] == "UPDATE":
            self.visualizer.update_cell(msg["x"], msg["y"], msg["view"])
        elif msg["type"] == "TRAINS":
            self.visualizer.update_trains(msg["trains"])
        elif msg["type"] == "DETACH":
            del self.visualizer


if __name__ == "__main__":
    Client(20441)
    # clients = [Thread(target=client, args=(20445)) for _ in range(5)]
    # # start clients
    # for cl in clients:
    #     cl.start()
