from fastapi import WebSocket
from fastapi.logger import logger as log
from fastapi import WebSocket
import json

class CustomWebSocket(WebSocket):
    async def send_json(self, data: typing.Any, mode: str = "text") -> None:
        if mode not in {"text", "binary"}:
            raise RuntimeError('The "mode" argument should be "text" or "binary".')
        text = json.dumps(data, ensure_ascii=False).encode("utf-8")
        if mode == "text":
            await self.send({"type": "websocket.send", "text": text})
        else:
            await self.send({"type": "websocket.send", "bytes": text.encode("utf-8")})


class ConnectionManager(CustomWebSocket):
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
            await ws.send_json(message, mode="text")


manager = ConnectionManager()
