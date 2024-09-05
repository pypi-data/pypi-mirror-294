import logging
from datetime import datetime

from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.graphchatdemo.state import (
    ChatBotUiState,
    MainState,
)

logger = logging.getLogger()


def edge_entry(state: MainState):
    return "chat_node"


def generate_task_title(user_input: str) -> str:
    """生成任务标题"""
    max_length = 20
    truncated_input = user_input[:max_length]
    current_date = datetime.now().strftime("%m%d")  # noqa: DTZ005
    task_title = f"{truncated_input}@{current_date}"

    return task_title


class EntryNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")
        if not thread_id:
            raise Exception("require thread_id")
        user_input = state.get("user_input")
        state_ret = {
            # "messages": [ChatMessage(role="system", content=Prompts.chatbot())],
            "uistate": ChatBotUiState(threadId=thread_id),
            "task_title": generate_task_title(user_input),
        }
        return state_ret
