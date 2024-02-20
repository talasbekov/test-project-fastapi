from fastapi import WebSocket
import typing
import json

class CustomWebSocket(WebSocket):
    async def send_json1(self, data: typing.Any, mode: str = "text") -> None:
        if mode not in {"text", "binary"}:
            raise RuntimeError('The "mode" argument should be "text" or "binary".')
        text = json.dumps(data, ensure_ascii=False).encode("utf-8")
        if mode == "text":
            await self.send({"type": "websocket.send", "text": text.decode("utf-8")})
        else:
            await self.send({"type": "websocket.send", "bytes": text.decode("utf-8")})

    async def send_json2(self, data: typing.Any, mode: str = "text") -> None:
        if mode not in {"text", "binary"}:
            raise RuntimeError('The "mode" argument should be "text" or "binary".')
        text = json.dumps(data, separators=(",", ":"))
        if mode == "text":
            await self.send({"type": "websocket.send", "text": text})
        else:
            await self.send({"type": "websocket.send", "bytes": text.encode("utf-8")})
