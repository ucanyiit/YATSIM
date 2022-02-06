import json

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
            data = json.loads(event["text"])
            print(data)
            if data["type"] == "attach":
                # check data["room"] and data["token"]
                send_data = json.dumps({"asd": "asd"})
                print(send_data, type(send_data))
                await send({"type": "websocket.send", "text": send_data})


def send_message_to_connections(data):
    for send in connections:
        send(data)
