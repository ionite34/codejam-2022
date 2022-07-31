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
    index_html = DATA.joinpath("index.html").read_text()
    return HTMLResponse(index_html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle websocket connections."""
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
        except ws.WebSocketDisconnect:
            break
        await websocket.send_text(f"Message received: {data}")


def start():
    """Launch with `poetry run start`"""
    uvicorn.run("goblingame.server:app", host="127.0.0.1", port=8000, reload=True)
