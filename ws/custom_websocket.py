from fastapi import WebSocket
import typing
import json

class CustomWebSocket(WebSocket):
    def __init__(self, scope, receive, send):
        super().__init__(scope=scope, receive=receive, send=send)

    async def send_json(self, data: typing.Any, mode: str = "text") -> None:
        if mode not in {"text", "binary"}:
            raise RuntimeError('The "mode" argument should be "text" or "binary".')
        text = json.dumps(data, ensure_ascii=False).encode("utf-8")
        if mode == "text":
            await self.send({"type": "websocket.send", "text": text.decode("utf-8")})
        else:
            await self.send({"type": "websocket.send", "bytes": text.decode("utf-8")})
