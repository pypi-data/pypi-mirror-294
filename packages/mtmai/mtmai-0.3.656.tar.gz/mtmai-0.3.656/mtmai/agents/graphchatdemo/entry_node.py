import logging
from datetime import datetime

from langchain_core.messages import ChatMessage
from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.graphchatdemo.prompts import Prompts
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
            "messages": [ChatMessage(role="system", content=Prompts.chatbot())],
            "uistate": ChatBotUiState(threadId=thread_id),
            "task_title": generate_task_title(user_input),
            # "uidelta": UiDelta(
            #     uiState=ChatBotUiState(
            #         threadId=thread_id,
            #         # agent=agent_name,
            #         # agent_url_base=settings.API_V1_STR + "/" + agent_name,
            #         # graph_image_url=f"{settings.API_V1_STR}/{agent_name}/graph_image",
            #         # example_input_items=[
            #         #     ExampleInputItem(
            #         #         title="例子1",
            #         #         description="ai介绍",
            #         #         content="请自我介绍,尽量详细.",
            #         #     ),
            #         #     ExampleInputItem(
            #         #         title="例子2", description="例子2描述", content="hello"
            #         #     ),
            #         #     ExampleInputItem(
            #         #         title="例子3", description="例子3描述", content="hello"
            #         #     ),
            #         #     ExampleInputItem(
            #         #         title="例子4", description="例子4描述", content="hello"
            #         #     ),
            #         # ],
            #         # uichatitems=[
            #         #     UIChatMessageItem(
            #         #         compType="UserInput", props={"content": "fake-user-input"}
            #         #     )
            #         # ],
            #     )
            # ),
        }
        return state_ret
