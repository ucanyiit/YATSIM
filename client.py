import json
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

messages = [
    '{ "command": "LOGIN", "username": "12345", "password": "123"}',
    '{ "command": "LOGOUT }',
]


def incoming_message_printer(sock):
    while True:
        reply = sock.recv(1024)
        msg = json.loads(reply.decode())
        if msg["type"] == "MSG":
            print(msg["message"])


def client(port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("127.0.0.1", port))
    incoming_messages = Thread(target=incoming_message_printer, args=(sock,))
    incoming_messages.start()

    while True:
        inp = input()
        if inp == "exit":
            break
        sock.send(inp.encode())

    sock.close()
    incoming_messages.wait()


if __name__ == "__main__":
    client(20441)
    # clients = [Thread(target=client, args=(20445)) for _ in range(5)]
    # # start clients
    # for cl in clients:
    #     cl.start()
