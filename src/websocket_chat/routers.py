"""Websocket chat router for handling real-time chat messages."""

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .bl import MessageChunksQueue, llm_stream

websocket_chat_router = APIRouter(
    tags=["chat"],
)


@websocket_chat_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle incoming WebSocket connections and messages.

    Args:
        websocket (WebSocket): The WebSocket connection object.
    """
    await websocket.accept()

    message_priority = 0
    queue = MessageChunksQueue()

    try:
        while True:
            user_message = await websocket.receive_text()

            asyncio.create_task(
                llm_stream(
                    user_message=user_message, websocket=websocket, message_priority=message_priority, queue=queue
                )
            )

            message_priority += 1

    except WebSocketDisconnect:
        pass
