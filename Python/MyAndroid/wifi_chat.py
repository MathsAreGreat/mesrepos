#!/usr/bin/env python3
import asyncio
import websockets
import http.server
import socketserver
import threading
import argparse
from datetime import datetime
import os

# -------------------------
# Utility
# -------------------------
def timestamp():
    return datetime.now().strftime("%H:%M:%S")

# -------------------------
# WebSocket Chat Server
# -------------------------
class ChatServer:
    def __init__(self):
        self.clients = set()

    async def register(self, ws):
        self.clients.add(ws)

    async def unregister(self, ws):
        self.clients.discard(ws)

    async def broadcast(self, msg):
        for client in list(self.clients):
            try:
                await client.send(msg)
            except:
                self.clients.discard(client)

    async def handler(self, ws):
        await self.register(ws)
        try:
            async for message in ws:
                await self.broadcast(f"[{timestamp()}] {message}")
        finally:
            await self.unregister(ws)

# -------------------------
# HTTP Server
# -------------------------
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="static", **kwargs)

# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5050)
    args = parser.parse_args()

    chat_server = ChatServer()

    async def runner():
        # WebSocket server (port +1)
        async with websockets.serve(chat_server.handler, args.host, args.port + 1):
            print(f"🔌 WebSocket running on ws://{args.host}:{args.port+1}")

            # HTTP server (serve static folder)
            socketserver.TCPServer.allow_reuse_address = True
            httpd = socketserver.TCPServer((args.host, args.port), Handler)
            print(f"📜 HTTP running on http://{args.host}:{args.port}")
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()

            await asyncio.Future()  # keep running

    asyncio.run(runner())

if __name__ == "__main__":
    main()