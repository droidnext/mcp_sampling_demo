import os
import sys
import logging
import asyncio
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI, AzureOpenAI

from mcp import ClientSession, types, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG to see all logs
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger("NewsAgent Client")
    logger.setLevel(logging.DEBUG)  # Ensure debug level is set
    return logger

logger = configure_logging()

# Load environment variables
logger.debug("Loading environment variables...")
try:
    load_dotenv()
    logger.debug("Environment variables loaded")
except Exception as e:
    logger.error(f"Failed to load environment variables: {e}")
    raise

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize OpenAI client
def initialize_openai_client():
    logger.debug("Initializing OpenAI client...")
    return AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

# Initialize OpenAI client
client = initialize_openai_client()


# Optional: create a sampling callback
async def handle_sampling_message(
    context: Any,
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    logger.debug(f"Received sampling message: {message}")
    if hasattr(
        message.messages[0].content,
        "text",
    ):
        prompt = message.messages[0].content.text
    else:
        raise ValueError("Invalid message content type")
    
    logger.debug(f"Prompt: {prompt}")
    llm_response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    logger.debug(f"LLM Response: {llm_response}")
    llm_response = llm_response.choices[0].message.content
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text=llm_response,
        ),
        model=model_name,
        stopReason="endTurn",
    )


async def run():
    """
    Main function to demonstrate MCP client functionality.

    Establishes an SSE connection to the server, initializes a session,
    and demonstrates basic operations like sending pings, listing tools,
    and calling a weather tool.
    """
    async with sse_client(url="http://localhost:8000/sse") as (read, write):
        async with ClientSession(
            read, write, sampling_callback=handle_sampling_message
        ) as session:
            await session.initialize()
            await session.send_ping()

            # List available tools
            tools = await session.list_tools()
            logger.info(f"List available tools {tools}")

            # Call a tool
            result = await session.call_tool("aggregate_news", arguments={"message": {"topic": "AI advancements"}})
            logger.debug("\n\n\n")
            logger.info(result.content[0].text)
            logger.debug("\n\n\n")

if __name__ == "__main__":
    asyncio.run(run())