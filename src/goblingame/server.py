import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from goblingame.data import DATA

app = FastAPI()


@app.get("/")
async def get():
    """Return the homepage."""
    index_html = DATA.joinpath("index.html").read_text()
    return HTMLResponse(index_html)


@app.get("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle websocket connections."""
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")


def start():
    """Launch with `poetry run start`"""
    uvicorn.run("goblingame.server:app", host="0.0.0.0", port=8000, reload=True)
