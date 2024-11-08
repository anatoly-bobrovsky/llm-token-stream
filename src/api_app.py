"""API App entry point."""

import uvicorn
from fastapi import FastAPI

from websocket_chat import websocket_chat_router

app = FastAPI(
    title="Websocket chat API.",
    description="Websocket chat API for token streaming with asynchronous message handling",
)

app.include_router(websocket_chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
