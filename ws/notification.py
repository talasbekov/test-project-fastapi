from fastapi import WebSocket
from fastapi.logger import logger as log
from fastapi import WebSocket
import typing
import json
from .custom_websocket import CustomWebSocket


class ConnectionManager():
    def __init__(self):
        self.active_connections: dict[str, CustomWebSocket] = {}

    async def connect(self, websocket: CustomWebSocket, user_id: str):
        self.active_connections[user_id] = websocket
        await websocket.send_text('CONNECTED')
        return user_id

    def disconnect(self, user_id: str, websocket: CustomWebSocket):
        try:
            self.active_connections.pop(user_id)
        except KeyError as e:
            log.error(e)
        return user_id

    async def broadcast(self, message:dict, user_id: str):
        ws = self.active_connections.get(user_id)
        print(message)
        if ws is not None:
            await ws.send_json1(message, mode="text")


manager = ConnectionManager()
