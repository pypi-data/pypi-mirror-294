import logging

import httpx
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


logger = logging.getLogger()


@tool(response_format="content_and_artifact")
def search_tool(query: str):
    """Useful to search content from web."""
    logger.info("调用 search 工具 %s", query)

    tool_api_url = "http://localhost:8333/api/tools/search_internet"

    with httpx.Client() as client:
        params = {"q": query}
        r = client.get(tool_api_url + "", params=params)
        r.raise_for_status()
        return (
            r.text,
            {"url": "https://www.baidu.com"},
        )
