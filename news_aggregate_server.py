from fastapi import FastAPI
from fastmcp import Context, FastMCP
import sys
import logging
from typing import Any, List, Dict




def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("news_aggregate_server.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger("NewsAggregator")
    return logger


def initialize_mcp_server(logger):
    logger.info("1. Initializing FastMCP server...")
    try:
        mcp = FastMCP("NewsAggregator")
        logger.info("2. FastMCP server initialized")
        return mcp
    except Exception as e:
        logger.error(f"Failed to initialize FastMCP: {e}")
        raise


async def aggregate_news(message: Dict[str, Any], context: Context) -> List[Dict]:
    """
    This tool is used to aggregate news articles from multiple sources and analyze their tone, remove bias, or rewrite neutrally of news articles and promote fairness and transparency.
    """
    logger.info("Tool aggregate_news called")


logger = configure_logging()
mcp = initialize_mcp_server(logger)

# Register the tool
@mcp.tool()
async def aggregate_news(
    message: Dict[str, Any],
     context: Context) -> List[Dict]:
    """
    This tool is used to aggregate news articles from multiple sources and analyze their tone, remove bias, or rewrite neutrally of news articles and promote fairness and transparency.
    """ 
    logger.info("Tool aggregate_news called")
    logger.debug(f"Received request: {message}")
    logger.debug(f"Context: {context}")
   
    # Simulatng new articles from API calls 
    news_array = [
        {
            "title": "Disaster Looms as Incompetent Leaders Fumble Climate Policy",
            "source": "HotTake News",
            "url": "https://hottakenews.com/climate-crisis",
            "content": "In yet another display of utter negligence, world leaders failed to reach a consensus on climate action, dooming future generations to a planet in crisis."
        },
        {
            "title": "Tech Billionaires Save the Economy Again",
            "source": "Silicon Beat",
            "url": "https://siliconbeat.com/billionaire-heroes",
            "content": "Thanks to visionary entrepreneurs, the tech sector is booming while the rest of the economy struggles. Once again, innovation proves its worth over government red tape."
        },
        {
            "title": "Opposition's Reckless Promises Threaten National Stability",
            "source": "Patriot Daily",
            "url": "https://patriotdaily.com/opposition-chaos",
            "content": "The opposition party continues to push absurd, budget-wrecking proposals that would destabilize the country and undo decades of responsible governance."
        },
        {
            "title": "Progressive Reforms Bring Hope and Dignity to Millions",
            "source": "Progress Watch",
            "url": "https://progresswatch.org/new-era",
            "content": "Bold reforms spearheaded by progressives are finally giving a voice to the marginalized and restoring dignity to working families across the nation."
        }
    ]


    logger.debug(" About to call context.sample")
    try:
        response = await context.sample(
            f"Analyze tone, remove bias, or rewrite neutrally of these news articles: {news_array} ",
            system_prompt="You are a news analyst who can analyze the tone, remove bias, or rewrite neutrally of news articles and promote fairness and transparency. Return back a JSON array of the news articles. Example [{\'title\':\'\',\'source\':\'\',\'url\': \'\',\'content\': \'\'}].",
        )
        logger.debug("context.sample completed")
        logger.debug(f"Response: {response}")
        
        if hasattr(response, "text"):
            logger.debug("Returning response text")
            return response.text
            
        logger.warning("No text attribute in response")
        return "No response"
    except Exception as e:
        logger.error(f"Error in aggregate_news: {e}", exc_info=True)
        raise

# Create FastAPI app and mount the SSE  MCP server
app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    """
    Health check endpoint to verify the server is running.

    Returns:
        dict: A simple message indicating the server is running.
    """
    return {"message": "Server is running"}


app.mount("/", mcp.sse_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)