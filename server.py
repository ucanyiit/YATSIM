from socket import AF_INET, SOCK_STREAM, socket

from yatsim import connection as c
from yatsim import room_manager as rm
from yatsim.db.connect import DB
from yatsim.user import UserManager

if __name__ == "__main__":
    db = DB("./database.db")
    room_manager = rm.RoomManager(db)
    user_manager = UserManager(db)
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
