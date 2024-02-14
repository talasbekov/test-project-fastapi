from fastapi import WebSocket
from fastapi.logger import logger as log

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        self.active_connections[user_id] = websocket
        await websocket.send_text('CONNECTED')
        return user_id

    def disconnect(self, user_id: str, websocket: WebSocket):
        try:
            self.active_connections.pop(user_id)
        except KeyError as e:
            log.error(e)
        return user_id
    
    async def broadcast(self, message:str, user_id: str):
        ws = self.active_connections.get(user_id)
        print(message)
        if ws is not None:
            await ws.send_text(message)


manager = ConnectionManager()
