import logging
from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.graphchatdemo.state import (
    MainState,
)
from mtmai.models.agent import UiMessageBase

logger = logging.getLogger()


def edge_human_node(state: MainState):
    return "supervisor"


primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("placeholder", "{messages}"),
        (
            "system",
            dedent(r"""
      你是专业客服聊天机器人,基于以上对话直接向用户输出回复内容
      [要求]:
      - 必须使用中文回复用户,再强调一次, 必须只能使用中文回复用户
      - 回复内容必须详细
      - 尽可能使用markdown语法输出内容
      - 禁止出现中英翻译对照的情况,例如禁止这种方式: "你好 hello"
    """),
        ),
    ]
)


class HumanNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: MainState, config: RunnableConfig):
        messages = state.get("messages")

        artifaces_state = {}
        if len(messages) > 0 and messages[-1].type == "tool":
            if messages[-1].artifact:
                artifaces_state = {"artifaces": [messages[-1].artifact]}

        system_message = primary_assistant_prompt.format_messages(messages=messages)
        ai_message = await self.runnable.ainvoke(system_message, config)

        ui_messages = []
        if ai_message.content:
            ui_messages.append(
                UiMessageBase(
                    component="AiCompletion", props={"content": ai_message.content}
                )
            )

        return {
            **artifaces_state,
            "messages": [ai_message],  # !!! 这个消息可能不用加上去
            "ui_messages": ui_messages,
            "uistate": state.get("uistate"),
        }
