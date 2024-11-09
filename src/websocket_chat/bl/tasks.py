"""Tasks.

This module contains the implementation of the llm_stream function, which streams
responses from a language model to a WebSocket client.
"""

import asyncio

from fastapi import WebSocket
from langchain_openai import ChatOpenAI

from env_settings import env

from ..schemas import Message

model = ChatOpenAI(model=env.OPENAI_MODEL)


async def llm_stream(user_message: Message, websocket: WebSocket) -> None:
    """
    Stream responses from the language model to a WebSocket client.

    Args:
        user_message (Message): The message object containing the user's input.
        websocket (WebSocket): The WebSocket connection to send responses to.
    """
    async for chunk in model.astream(user_message.text):
        await asyncio.sleep(env.TIME_BETWEEN_CHUNKS)  # control the output speed
        response_chunk = Message(id=user_message.id, text=chunk.content)
        await websocket.send_json(response_chunk.model_dump())
