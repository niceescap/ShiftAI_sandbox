"""Émetteur de télémesure JSON live."""
import json
import asyncio

class TelemetryEmitter:
    def __init__(self):
        self.clients = []

    def register_client(self, ws):
        self.clients.append(ws)

    def unregister_client(self, ws):
        if ws in self.clients:
            self.clients.remove(ws)

    async def emit(self, data: dict):
        message = json.dumps(data)
        for ws in self.clients[:]:
            try:
                await ws.send(message)
            except Exception:
                pass
