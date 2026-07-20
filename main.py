"""Serveur principal - banc d'essai Fit Live.
Exécute : uvicorn main:app --host 0.0.0.0 --port 8000
WebSocket : ws://<serveur>:8765/ws (port séparé ou même port via sub-protocol)
Pour simplifier : tout sur le port HTTP avec WebSocket intégré.
"""
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

from simulator import Simulator
from telemetry import TelemetryEmitter
from config import HTTP_PORT

app = FastAPI(title="Fit Live Simulator")
app.mount("/static", StaticFiles(directory="static"), name="static")

simulator = Simulator()
emitter = TelemetryEmitter()

# Tâche du loop 1Hz
async def simulation_loop():
    sec = 0
    while True:
        data = simulator.tick(sec)
        await emitter.emit(data)
        sec = (sec + 1) % 300  # boucle sur 5 min
        await asyncio.sleep(1.0)

@app.on_event("startup")
async def start_loop():
    asyncio.create_task(simulation_loop())

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r") as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    emitter.register_client(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if "current_cog" in msg:
                    simulator.set_current_cog(msg["current_cog"])
            except Exception:
                pass
    except WebSocketDisconnect:
        emitter.unregister_client(websocket)

@app.get("/status")
async def status():
    return {
        "speed_kmh": simulator.v_kmh,
        "current_cog": simulator.derailer.get_index(),
        "cadence_rpm": simulator.derailer.get_ratio(),
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=HTTP_PORT)
