import logging

from langchain_core.messages import ChatMessage
from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.graphchatdemo.prompts import Prompts
from mtmai.agents.graphchatdemo.state import (
    ChatBotUiState,
    MainState,
    # UIChatMessageItem,
    # UiDelta,
)
from mtmai.models.agent import AgentTask

logger = logging.getLogger()


def edge_entry(state: MainState):
    return "chat_node"


class EntryNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")
        if not thread_id:
            raise Exception("require thread_id")
        user_id = config.get("configurable").get("user_id")
        # db = state["context"].db
        session = state.get("context").session
        state_ret = {
            "messages": [ChatMessage(role="system", content=Prompts.chatbot())],
            "uistate": ChatBotUiState(threadId=thread_id),
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
        # with Session(db) as session:
        item = AgentTask(thread_id=thread_id, user_id=user_id, title="no title task")
        session.add(item)
        session.commit()
        return state_ret
