"""
Webhook API Routes for Real-time Updates
Supports Server-Sent Events (SSE) and WebSocket connections
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from typing import List, Set, Dict, Any
import json
import asyncio
from datetime import datetime
import uuid

router = APIRouter()

# Store active connections
sse_connections: Set[asyncio.Queue] = set()
ws_connections: Set[WebSocket] = set()


class WebhookEvent:
    """Webhook event model"""
    def __init__(self, event_type: str, payload: Any, source: str = "system"):
        self.id = str(uuid.uuid4())
        self.type = event_type
        self.payload = payload
        self.timestamp = datetime.utcnow().isoformat()
        self.source = source
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "source": self.source
        }


async def broadcast_event(event: WebhookEvent, event_types: List[str] = None):
    """Broadcast event to all connected clients"""
    event_dict = event.to_dict()
    
    # Filter by event types if specified
    if event_types and event.type not in event_types:
        return
    
    # Broadcast to SSE connections
    disconnected = []
    for queue in sse_connections:
        try:
            await queue.put(event_dict)
        except Exception as e:
            print(f"Error broadcasting to SSE: {e}")
            disconnected.append(queue)
    
    # Remove disconnected queues
    for queue in disconnected:
        sse_connections.discard(queue)
    
    # Broadcast to WebSocket connections
    disconnected_ws = []
    for ws in ws_connections:
        try:
            await ws.send_json(event_dict)
        except Exception as e:
            print(f"Error broadcasting to WebSocket: {e}")
            disconnected_ws.append(ws)
    
    # Remove disconnected WebSockets
    for ws in disconnected_ws:
        ws_connections.discard(ws)


@router.get("/stream")
async def stream_webhooks(request: Request, events: str = None):
    """
    Server-Sent Events (SSE) endpoint for webhook streaming
    Usage: GET /api/v1/webhooks/stream?events=fraud_detected,order_updated
    """
    event_types = events.split(",") if events else []
    
    async def event_generator():
        queue = asyncio.Queue()
        sse_connections.add(queue)
        
        try:
            # Send initial connection message
            yield f"data: {json.dumps({'type': 'connected', 'message': 'Webhook stream connected'})}\n\n"
            
            while True:
                # Wait for event with timeout
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    # Send heartbeat
                    yield f": heartbeat\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            sse_connections.discard(queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for bi-directional webhook communication
    Usage: ws://localhost:5000/api/v1/webhooks/ws
    """
    await websocket.accept()
    ws_connections.add(websocket)
    subscribed_events: List[str] = []
    
    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "message": "WebSocket connected"
        })
        
        while True:
            # Receive message from client
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("action") == "subscribe":
                    subscribed_events = message.get("eventTypes", [])
                    await websocket.send_json({
                        "type": "subscribed",
                        "eventTypes": subscribed_events
                    })
                elif message.get("action") == "unsubscribe":
                    subscribed_events = []
                    await websocket.send_json({
                        "type": "unsubscribed"
                    })
                elif message.get("action") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
    except WebSocketDisconnect:
        pass
    finally:
        ws_connections.discard(websocket)


@router.post("/trigger")
async def trigger_webhook(event_type: str, payload: Dict[str, Any]):
    """
    Manually trigger a webhook event (for testing)
    POST /api/v1/webhooks/trigger?event_type=fraud_detected
    Body: {"transaction_id": "txn_123", "risk_score": 0.85}
    """
    event = WebhookEvent(event_type, payload, source="api")
    await broadcast_event(event)
    
    return {
        "success": True,
        "message": f"Webhook event '{event_type}' triggered",
        "event_id": event.id
    }


# Helper function to trigger events from other parts of the application
async def trigger_webhook_event(event_type: str, payload: Any):
    """Helper function to trigger webhook events"""
    event = WebhookEvent(event_type, payload)
    await broadcast_event(event)
    return event.id

