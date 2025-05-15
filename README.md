# Model Context Protocol (MCP) Sampling Demo 

This project demonstrates the use of MCP sampling with FastAPI and OpenAI.

## Setup Instructions

1. **Initialize the environment**
   ```bash
   uv init
   uv venv
   source .venv/bin/activate
   uv pip install fastapi uvicorn openai fastmcp
   ```

## Running the Server

To start the server, run:
```bash
uv run news_aggregate_server.py
```

## Running the Client

To start the client, run:
```bash
uv run news_agent_client.py
```

## Additional Information

Ensure all environment variables are set correctly in the `.env` file before running the server or client. Refer to the `.env_local` file for an example.
