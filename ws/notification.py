import json
import uuid
from datetime import datetime

from typing import List
from fastapi import WebSocket, WebSocketDisconnect, Depends, Query, Header
from fastapi.logger import logger as log
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException 


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
        print(user_id)
        ws = self.active_connections.get(user_id)
        if ws is not None:
            ws.send_text(message)


manager = ConnectionManager()
