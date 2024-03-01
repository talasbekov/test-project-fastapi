from fastapi.websockets import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections = []
        self.rooms = {}

    async def connect(self, websocket: WebSocket): 
        await websocket.accept()
        self.active_connections.append(websocket) 

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        for room, connections in self.rooms.items():
            if websocket in connections:
                connections.remove(websocket)

    async def join_room(self, websocket: WebSocket, room_name: str):
        if room_name not in self.rooms:
            self.rooms[room_name] = [] 
        self.rooms[room_name].append(websocket)

    async def leave_room(self, websocket: WebSocket, room_name: str):
        if room_name in self.rooms and websocket in self.rooms[room_name]:
            self.rooms[room_name].remove(websocket)

    async def send_to_room(self, room_name: str, message: str):
        if room_name in self.rooms:
            for connection in self.rooms[room_name]:
                await connection.send_text(message)

    async def send_json_to_room(self, room_name: str, message: dict, role="operator"): 
        if room_name in self.rooms:
            for connection in self.rooms[room_name]:
                await connection.send_json(message)

    async def send_json_notification_for_all(self, message: dict):
        for room, connections in self.rooms.items():
            for connection in connections:
                await connection.send_json(message)

    async def send_to_all(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_bytes_to_all(self, message: bytes):
        for connection in self.active_connections:
            await connection.send_bytes(message)

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(WebSocketManager, cls).__new__(cls)
        return cls.instance


manager = WebSocketManager()
