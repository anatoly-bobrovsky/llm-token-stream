# LLM Token Stream Processing

## Overview
This repository provides a template for a chatbot backend built with `FastAPI` using `WebSocket` communication. The project is optimized for token streaming with asynchronous message handling.

## Features

- **WebSocket Communication**: Real-time interactions through WebSocket endpoints.
- **Asynchronous Message Handling**: The bot can handle multiple user messages asynchronously, allowing users to send messages consecutively without waiting for responses. All requests will receive replies.
- **Dockerized Deployment**: Simplified deployment using Docker.

## Getting Started

### Prerequisites

- Docker installed on your machine.

### Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/anatoly-bobrovsky/llm-token-stream
   cd llm-token-stream
   ```

2. **Build the Docker Image**:
   ```bash
   docker build -t your-tag .
   ```

3. **Environment Setup**:
   Create an environment file (`.env`) with the following variables:
   - `OPENAI_API_KEY` - a valid API key for OpenAI, which can be created at platform.openai.com
   - `OPENAI_MODEL` - the LLM model used for responses, for example, `gpt-4o-mini`
   - `TIME_BETWEEN_CHUNKS` - time between chunks in seconds to control the output speed, for example, `0.1`

4. **Run the Service**:
   ```bash
   docker run --publish-all --rm --env-file .env your-tag
   ```

5. **Verify the Port**:
   ```bash
   docker ps
   ```

### Usage

You can use [Postman](https://www.postman.com/) or any WebSocket client to connect via WebSocket at `ws://localhost:{port}/ws`. Alternatively, you can test it with the included `index.html` using VS Code Live Server:

1. Open `index.html` using VS Code Live Server.
2. In the first text field, enter the WebSocket URL (`ws://localhost:{port}/ws`) and click "Connect." A popup will confirm a successful connection.
3. In the second text field, enter your message and click "Send."
4. Responses from the bot will appear below in a tokenized format.

## Project Structure

```plaintext
.
├── Dockerfile
├── index.html  # Client interface for WebSocket interaction
├── requirements.txt
└── src
    ├── env_settings.py          # Manages environment variables
    ├── api_app.py               # Entrypoint for the chatbot app
    └── websocket_chat           # WebSocket Chat Package
        ├── routers.py           # Defines endpoints
        └── bl                   # Business Logic Package
            ├── data_structures.py  # Custom data structures
            ├── enums.py
            └── tasks.py         # Task for streaming response chunks from LLM
```

## Possible Improvements

1. Add logging and unit tests.
2. Replace the custom queue with a message broker, such as RabbitMQ.
3. Add a unique identifier and memory (checkpointing) for each conversation.
4. Improve the client interface (index.html) visually.
5. Refactor with design patterns and introduce new abstractions where applicable.