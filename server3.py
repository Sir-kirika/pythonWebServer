from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime, timezone
import asyncio
import json
import uvicorn
import contextlib

app = FastAPI()

AUTH_TOKEN = "supersecret123"

# Track all active websocket connections
connected_clients = set()

def get_gmt_timestamp():
    return datetime.now(timezone.utc).strftime('%Y.%m.%d %H:%M:%S')

async def broadcast(message: str, sender: WebSocket = None):
    """Send a message to all connected clients (optionally excluding sender)."""
    disconnected = []
    for client in connected_clients:
        try:
            # If you want to skip echoing to the sender, uncomment next line
            # if client is sender: continue
            await client.send_text(message)
        except Exception as e:
            print(f"[SERVER] broadcast error: {e}")
            disconnected.append(client)
    # Remove failed connections
    for client in disconnected:
        connected_clients.discard(client)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Simple token auth via query param
    token = websocket.query_params.get("token")
    if token != AUTH_TOKEN:
        print("[SERVER] Unauthorized access attempt")
        await websocket.close(code=1008)  # Policy Violation
        return

    await websocket.accept()
    connected_clients.add(websocket)
    print("[SERVER] Client connected")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"[CLIENT->SERVER] {data}")
            # Attach timestamp for server trace
            payload = data
            await broadcast(payload, sender=websocket)
    except WebSocketDisconnect:
        print("[SERVER] Client disconnected")
    except Exception as e:
        print(f"[SERVER] receiver error: {e}")
    finally:
        connected_clients.discard(websocket)
        with contextlib.suppress(Exception):
            await websocket.close()
        print("[SERVER] Session closed")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="local.key",
        ssl_certfile="local.crt"
    )
