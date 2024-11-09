"""Websocket chat router for handling real-time chat messages."""

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, status
from pydantic import ValidationError

from .bl import llm_stream
from .schemas import Message

websocket_chat_router = APIRouter(
    tags=["chat"],
)


@websocket_chat_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handle incoming WebSocket connections and messages.

    Args:
        websocket (WebSocket): The WebSocket connection object.
    """
    await websocket.accept()

    try:
        while True:
            user_message = Message.parse_raw(await websocket.receive_text())
            asyncio.create_task(llm_stream(user_message=user_message, websocket=websocket))

    except ValidationError:
        raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)
    except WebSocketDisconnect:
        pass
