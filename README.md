# Model Context Protocol (MCP) Sampling Demo

This project demonstrates the use of MCP sampling with FastAPI and OpenAI for news aggregation and bias removal.

## Use Case: News Aggregation and Bias Removal

This code example shows how to use MCP tools to:
1. Server ToolCollect news articles
2. Make MCP sampling callbacks to client remove bias
3. Return neutral news summaries

## Example Flow

### 1. New Articls fetched by Server Tool 
```json
{
    "title": "Disaster Looms as Incompetent Leaders Fumble Climate Policy",
    "source": "HotTake News",
    "url": "https://hottakenews.com/climate-crisis",
    "content": "In yet another display of utter negligence, world leaders failed to reach a consensus on climate action, dooming future generations to a planet in crisis."
}
```

### 2. After MCP Sampling Callback Output
```json
{
    "title": "World Leaders Struggle to Reach Consensus on Climate Action",
    "source": "HotTake News",
    "url": "https://hottakenews.com/climate-crisis",
    "content": "World leaders faced challenges in reaching a consensus on climate policy during recent discussions, raising concerns about the potential impact on future generations regarding environmental issues."
}
```

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
