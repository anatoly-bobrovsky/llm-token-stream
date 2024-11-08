"""Tasks.

This module contains the implementation of the llm_stream function, which streams
responses from a language model to a WebSocket client. It utilizes the ChatOpenAI
model to generate responses based on user input and manages message chunks using
a queue.
"""

import asyncio

from fastapi import WebSocket
from langchain_openai import ChatOpenAI

from env_settings import env

from .data_structures import MessageChunksQueue
from .enums import Signal

# initialize the ChatOpenAI model
model = ChatOpenAI(model=env.OPENAI_MODEL)


async def llm_stream(user_message: str, websocket: WebSocket, message_priority: int, queue: MessageChunksQueue) -> None:
    """Stream responses from the language model to the WebSocket.

    Args:
        user_message (str): The message sent by the user to be processed.
        websocket (WebSocket): The WebSocket connection to send responses to.
        message_priority (int): The priority of the message being processed.
        queue (MessageChunksQueue): The queue to manage message chunks.
    """
    chunk_priority = 0

    queue.push(chunk=Signal.START.value, message_priority=message_priority, chunk_priority=chunk_priority)

    # stream the response chunks from the language model.
    async for chunk in model.astream(user_message):
        if not chunk.content:
            continue  # skip empty chunks.

        chunk_priority += 1
        queue.push(chunk=chunk.content, message_priority=message_priority, chunk_priority=chunk_priority)

        # send each response chunk to the WebSocket.
        for response_chunk in queue.flush():
            await asyncio.sleep(env.TIME_BETWEEN_CHUNKS)
            await websocket.send_text(response_chunk)

    chunk_priority += 1
    queue.push(chunk=Signal.END.value, message_priority=message_priority, chunk_priority=chunk_priority)

    for response_chunk in queue.flush():
        await asyncio.sleep(env.TIME_BETWEEN_CHUNKS)
        await websocket.send_text(response_chunk)
