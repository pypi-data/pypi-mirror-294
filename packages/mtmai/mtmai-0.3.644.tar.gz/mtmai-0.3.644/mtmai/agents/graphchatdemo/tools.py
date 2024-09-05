import logging

import httpx
from langchain_core.tools import tool

logger = logging.getLogger()


@tool
def search(query: str):
    """Useful to search content from web."""
    logger.info("调用 search 工具 %s", query)
    return [
        f"I looked up: {query}. Result: It's sunny in San Francisco, but you better look out if you're a Gemini 😈."
    ]


# default_tools = [search]
# class WebSearchTool:
#     @tool("Web Search")
#     def web_search(data):
#         """
#         Useful to search content from web.
#         """
#         # email, subject, message = data.split("|")
#         # gmail = GmailToolkit()
#         # draft = GmailCreateDraft(api_resource=gmail.api_resource)
#         # resutl = draft({
#         # 		'to': [email],
#         # 		'subject': subject,
#         # 		'message': message
#         # })
#         resutl = {
#             "to": "fake@email.com",
#             "subject": "fakesubject",
#             "message": "fake_message",
#         }
#         return f"\nSearch content results: {resutl}\n"


logger = logging.getLogger(__name__)


class SearchTools:
    @tool("Search the internet")
    def search_internet(query: str):
        """Useful to search the internet
        about a a given topic and return relevant results.
        """
        logger.info("web_search 工具调用 %s", query)
        tool_api_url = "http://localhost:8333/api/tools/search_internet"

        with httpx.Client() as client:
            params = {"q": query}
            r = client.get(tool_api_url + "", params=params)
            r.raise_for_status()  # Raise an exception if the request was unsuccessful
            return r.text
