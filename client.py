import json
import pprint
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


class Client:
    def __init__(self, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(("127.0.0.1", port))
        self.username = ""
        self.visualizer = None
        self.running = True
        self.view = None

        incoming_messages = Thread(target=self.outgoing_message_handler, args=(sock,))
        incoming_messages.start()

        while self.running:
            reply = sock.recv(1024)
            msg = json.loads(reply.decode())
            self.handle_message(msg)

        sock.close()
        incoming_messages.wait()

    def outgoing_message_handler(self, sock):
        while True:
            inp = input()
            if inp == "exit":
                self.running = False
                break
            sock.send(inp.encode())

    def handle_message(self, msg):
        if msg["type"] == "MSG":
            print(msg["message"])
        elif msg["type"] == "LOGIN":
            self.username = msg["username"]
            print(f"Logged in with {self.username}.")
        elif msg["type"] == "LOGOUT":
            self.username = ""
            print("Logged out.")
        elif msg["type"] == "VIEW":
            print("Room is attached.")
            pprint.pprint(msg["view"])
            self.view = msg["view"]
            # pygame.init()
            # self.visualizer = Visualizer(msg["height"], msg["width"], msg["view"])
        elif msg["type"] == "UPDATE":
            print("Cell updated")
            x, y, view = msg["x"], msg["y"], msg["view"]
            print(f"X: {x}, Y: {y}, VIEW: {view}")
            self.view[msg["y"]][msg["x"]] = msg["view"]
            print("New view")
            pprint.pprint(self.view)
            # self.visualizer.update_cell(msg["x"], msg["y"], msg["view"])
        elif msg["type"] == "TRAINS":
            print("Trains moved...")
            pprint.pprint(msg["trains"])
            # self.visualizer.update_trains(msg["trains"])
        elif msg["type"] == "DETACH":
            del self.visualizer


if __name__ == "__main__":
    Client(20441)
    # clients = [Thread(target=client, args=(20445)) for _ in range(5)]
    # # start clients
    # for cl in clients:
    #     cl.start()
