# backend/websockets.py

from fastapi import WebSocket
from typing import Dict

connected_clients: Dict[str, WebSocket] = {}

async def connect_client(email: str, websocket: WebSocket):
    await websocket.accept()
    connected_clients[email] = websocket
    print(f"✅ Connected: {email}")

async def disconnect_client(email: str):
    if email in connected_clients:
        await connected_clients[email].close()
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
