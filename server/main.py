import threading
import socket
import json
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import websockets
import os

from jwt_utils import generate_token, verify_token
from threshold import check_threshold

# ======================
# WEBSOCKET (ALERT)
# ======================
ws_clients = set()

async def ws_handler(ws):
    ws_clients.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        ws_clients.remove(ws)

async def ws_server():
    global ws_loop
    ws_loop = asyncio.get_running_loop()

    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        print("🌐 WebSocket aktif (8765)")
        await asyncio.Future()


def ws_broadcast(message):
    if ws_loop is None:
        return

    async def _send():
        for c in list(ws_clients):
            try:
                await c.send(json.dumps(message))
            except:
                ws_clients.remove(c)

    asyncio.run_coroutine_threadsafe(_send(), ws_loop)


# ======================
# UDP SERVER (SENSOR)
# ======================
def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 9999))
    print("🚀 UDP Server aktif (9999)")

    while True:
        data, addr = sock.recvfrom(1024)
        payload = json.loads(data.decode())

        token = payload.get("token")
        if not verify_token(token):
            print("❌ JWT tidak valid dari", addr)
            continue

        result = check_threshold(payload)
        result["device_id"] = payload.get("device_id", "unknown")

        ws_broadcast(result)

# ======================
# HTTP TOKEN SERVER
# ======================


class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Endpoint token
        if self.path.startswith("/token"):
            token = generate_token("sensor_device")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"token": token}).encode())
            return

        # Serve dashboard
        if self.path == "/" or self.path == "/index.html":
            try:
                path = os.path.join("web", "index.html")
                with open(path, "r", encoding="utf-8") as f:
                    html = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(html.encode())
            except FileNotFoundError:
                self.send_error(404, "index.html not found")
            return

        self.send_error(404)


def http_server():
    print("🌐 HTTP Server aktif (8080)")
    HTTPServer(("0.0.0.0", 8080), HTTPHandler).serve_forever()


# ======================
# MAIN
# ======================
def main():
    print("🔥 IOT ALERT SYSTEM (1 RUN)")

    threading.Thread(target=http_server, daemon=True).start()
    threading.Thread(target=udp_server, daemon=True).start()

    asyncio.run(ws_server())

if __name__ == "__main__":
    main()
