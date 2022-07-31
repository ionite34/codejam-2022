import starlette.websockets as ws
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from goblingame.data import DATA

import json, random

app = FastAPI()

origins = [
    "http://localhost:8000",
    "ws://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get():
    """Return the homepage."""
    index_html = DATA.joinpath("front-end/index.html").read_text()
    return HTMLResponse(index_html)

# temp database
ws_conns = {
    # str(host:port): {data}
}

uuids = []
def uuid_gen():
    while True:
        x = int(random.random() * 1e6)
        if x not in uuids:
            break
    uuids.append(x)
    return x

rooms = {}
room_chars = [str(i) for i in range(10)] \
    + [chr(i) for i in range(ord('a'), ord('z')+1)] \
    + [chr(i) for i in range(ord('A'), ord('Z')+1)]
def room_gen():
    while True:
        x = "".join(random.choice(room_chars) for _ in range(3))
        if x not in rooms:
            break
    rooms[x] = {}
    return x

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle websocket connections."""
    await websocket.accept()
    client = websocket.client
    client_str = f"{client.host}:{client.port}"
    uuid = uuid_gen()
    ws_conns[f"{client.host}:{client.port}"] = {
        "websocket": websocket,
        "uuid": uuid,
    }

    # send uuid info
    send_data = {
        "source": "c",
        "type": "ws-setup",
        "content": ws_conns[client_str]["uuid"]
    }
    await websocket.send_text(json.dumps(send_data))

    while True:
        try:
            data = await websocket.receive_text()
            data = json.loads(data)

            if data["type"] == 'room-create':
                room_id = room_gen()
                ws_conns[client_str]['room'] = room_id
                rooms[room_id] = {
                    "users": [client_str]
                }
                send_message = {
                    "source": "c",
                    "type": "room-join-s",
                    "content": room_id
                }
                await websocket.send_text(json.dumps(send_message))
            if data["type"] == 'room-join':
                room_id = data['content']
                if room_id in rooms:
                    if 'room' in ws_conns[client_str]:
                        rooms[room_id].remove(ws_conns[client_str]['room'])
                    ws_conns[client_str]['room'] = room_id
                    rooms[room_id]["users"].append(client_str)
                    send_message = {
                        "source": "c",
                        "type": "room-join-s",
                        "content": room_id
                    }
                else:
                    send_message = {
                        "source": "c",
                        "type": "room-join-f",
                        "content": room_id
                    }
                await websocket.send_text(json.dumps(send_message))
            
            # share message with everyone in room
            if data['type'] == 'room-message':
                send_message = {
                    "source": uuid,
                    "type": "room-message",
                    "content": data["content"]
                }
                if 'room' in ws_conns[client_str]:
                    room_id = ws_conns[client_str]['room']
                    if room_id in rooms:
                        for i in rooms[room_id]['users']:
                            if i == client_str:
                                continue
                            temp_ws = ws_conns[i]['websocket']
                            await temp_ws.send_text(json.dumps(send_message))
        except ws.WebSocketDisconnect:
            ws_conns[client_str]
            # code form disconnecting person
            break
        # await websocket.send_text(f"Message received: {data}")

@app.get("/src/css/main.css")
async def get():
    return HTMLResponse(
        DATA.joinpath("front-end/src/css/main.css").read_text(),
        media_type="text/css"
    )
@app.get("/src/js/index.js")
async def get():
    return HTMLResponse(
        DATA.joinpath("front-end/src/js/index.js").read_text(),
        media_type="text/js"
    )

def start():
    """Launch with `poetry run start`"""
    uvicorn.run("goblingame.server:app", host="127.0.0.1", port=8000, reload=True)
