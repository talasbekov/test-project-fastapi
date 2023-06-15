import uuid

from fastapi import WebSocket
from fastapi.logger import logger as log


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[uuid.UUID, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: uuid.UUID):
        await websocket.accept()

        self.active_connections[user_id] = websocket

        return user_id

    def disconnect(self, user_id: uuid.UUID,  websocket: WebSocket):
        try:
            self.active_connections.pop(user_id)
        except KeyError as e:
            log.error(e)
        return user_id

    async def broadcast(self, message:str, user_id: uuid.UUID):
        ws = self.active_connections.get(user_id)
        if ws is not None:
            ws.send_text(message)


manager = ConnectionManager()
