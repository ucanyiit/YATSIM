from socket import AF_INET, SOCK_STREAM, socket

from yatsim import connection as c
from yatsim import room_manager as rm
from yatsim.user import UserManager

if __name__ == "__main__":
    room_manager = rm.RoomManager()
    user_manager = UserManager()
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("", 20441))
    s.listen()
    try:
        while True:
            ns, peer = s.accept()
            print(peer, "connected")
            # Create a Connection (thread) with new socket
            t = c.Connection(ns, room_manager, user_manager)
            t.start()
    finally:
        s.close()
