import starlette.websockets as ws
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from goblingame.data import DATA

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
import json
ws_conns = {
    # str(host:port): {data}
}

uuids = []
def uuid_gen():
    import random
    while True:
        x = int(random.random() * 1e6)
        if x not in uuids:
            break
    uuids.append(x)
    return x

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle websocket connections."""
    await websocket.accept()
    client = websocket.client
    client_str = f"{client.host}:{client.port}"
    ws_conns[f"{client.host}:{client.port}"] = {
        "websocket": websocket,
        "uuid": uuid_gen(),
    }

    # send uuid info
    send_data = {
        "source": "s",
        "type": "ws_setup",
        "content": ws_conns[client_str]["uuid"]
    }
    await websocket.send_text(json.dumps(send_data))

    while True:
        try:
            data = await websocket.receive_text()
            data = json.loads(data)
        except ws.WebSocketDisconnect:
            ws_conns[client_str]
            break
        await websocket.send_text(f"Message received: {data}")

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
