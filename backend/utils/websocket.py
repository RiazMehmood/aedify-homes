from fastapi import WebSocket
from typing import Dict
from starlette.websockets import WebSocketState
connected_clients: Dict[str, WebSocket] = {}

async def connect_client(email: str, websocket: WebSocket):
    await websocket.accept()
    connected_clients[email] = websocket
    print(f"✅ Connected: {email}")

async def disconnect_client(email: str):
    websocket = connected_clients.get(email)
    if websocket:
        try:
            if websocket.application_state != WebSocketState.DISCONNECTED:
                await websocket.close()
        except Exception as e:
            print(f"⚠️ Failed to close WebSocket for {email}: {e}")
        finally:
            del connected_clients[email]
            print(f"❌ Disconnected: {email}")

async def send_event(email: str, event: dict):
    if email in connected_clients:
        try:
            await connected_clients[email].send_json(event)
            print(f"📤 Sent to {email}: {event}")
        except Exception as e:
            print(f"⚠️ Error sending to {email}: {e}")
            await disconnect_client(email)

