import logging
from textwrap import dedent

from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.prebuilt import tools_condition
from pydantic import BaseModel

from mtmai.agents.graphchatdemo.state import (
    MainState,
)

logger = logging.getLogger()


def edge_coder(state: MainState):
    is_tools = tools_condition(state)
    if is_tools == "tools":
        return "chat_tools_node"
    if state.get("next"):
        return state.get("next")
    else:
        return "human_node"


prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            dedent("""你是专业的程序员, 基于以上消息直接输出程序代码
                [要求]:
                - 仅输出代码, 禁止解释、寒暄、废话
                """),
        ),
    ]
).partial()


class RouteResponse(BaseModel):
    code: str | None = None


class CoderNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: MainState, config: RunnableConfig):
        supervisor_chain = (
            prompt | self.runnable
        )  # .with_structured_output(RouteResponse)
        aimessage = supervisor_chain.invoke(state)
        aimessage = ChatMessage(role="assistant", content=aimessage.content)
        return {"messages": [aimessage]}
