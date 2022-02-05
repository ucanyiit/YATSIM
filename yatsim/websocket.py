connections = {}


async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            client = scope["client"]
            connections[client] = send
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            client = scope["client"]
            connections.pop(client)
            break

        if event["type"] == "websocket.receive":
            print(event)
            if event["text"] == "ping":
                await send({"type": "websocket.send", "text": "pong!"})


def send_message_to_connections(data):
    for send in connections:
        send(data)
