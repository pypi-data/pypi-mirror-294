import logging
from datetime import datetime

from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.prebuilt import tools_condition

from mtmai.agents.graphchatdemo.state import (
    ChatBotUiState,
    MainState,
    UiChatItem,
    UiDelta,
)

from .state import agent_name
from .tools import default_tools

logger = logging.getLogger()


primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful customer support assistant for Swiss Airlines. "
            " Use the provided tools to search for flights, company policies, and other information to assist the user's queries. "
            " When searching, be persistent. Expand your query bounds if the first search returns no results. "
            " If a search comes up empty, expand your search before giving up."
            "\n\nCurrent user:\n<User>\n{user_info}\n</User>"
            "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())  # noqa: DTZ005


def edge_chat_node(state: MainState):
    is_tools = tools_condition(state)
    if is_tools == "tools":
        return "tools"
    if state.get("go_mtmeditor"):
        return "mtmeditor"
    else:
        return "uidelta"


class ChatNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")

        user_input = state.get("user_input")
        user_option = state.get("user_option")
        if user_option:
            # 是可视化编辑器的指令
            return {"go_mtmeditor": True}
        if user_input == "":
            logger.info("前端页面刷新后重新获取状态")
        if user_input.startswith("/"):
            return await self.uicommand(state, config)

        messages = state.get("messages")
        if len(messages) < 1:
            raise Exception("消息长度不正确")  # noqa: EM101, TRY002
        llm = self.runnable.bind_tools([*default_tools])
        if messages[-1].type == "tool":
            ai_message = await llm.ainvoke(messages, config)
            ui_messages = [
                UiChatItem(
                    component="AiCompletion", props={"content": ai_message.content}
                )
            ]
            return {
                "messages": [
                    ai_message,
                ],
                "ui_messages": ui_messages,
            }
        new_user_message = ChatMessage(role="user", content=state.get("user_input"))
        messages.append(new_user_message)
        ai_message = await llm.ainvoke(messages, config)

        ui_messages = [
            UiChatItem(component="UserMessage", props={"content": user_input}),
            # UiChatItem(component="AiCompletion", props={"content": ai_message.content}),
        ]
        if ai_message.content:
            ui_messages.append(
                UiChatItem(
                    component="AiCompletion", props={"content": ai_message.content}
                )
            )
        finnal_state = {
            "messages": [
                new_user_message,
                ai_message,
            ],
            "ui_messages": ui_messages,
            "uidelta": state.get("uidelta"),
        }
        return finnal_state

    async def uicommand(self, state: MainState, config: RunnableConfig):
        user_input = state.get("user_input")
        if user_input == "/1":
            return {
                "uidelta": UiDelta(
                    uiState=ChatBotUiState(
                        UiChatItem(
                            component="Image",
                            props={"src": f"/api/v1/{agent_name}/graph_image"},
                        ),
                    )
                ),
            }
        if user_input == "/2":
            # load ui state

            # pre_uistate = state.get("uistate")
            pre_uimessages = state.get("ui_messages")
            return {
                "uidelta": UiDelta(
                    uiState=ChatBotUiState(
                        ui_messages=pre_uimessages
                        # ui_messages=[
                        #     *pre_uimessages,
                        #     # UiChatItem(
                        #     #     component="Image",
                        #     #     props={"src": f"/api/v1/{agent_name}/graph_image"},
                        #     # ),
                        #     # UiChatItem(
                        #     #     component="UserMessage",
                        #     #     props={"content": "usercontent123"},
                        #     # ),
                        #     # UiChatItem(
                        #     #     component="AiCompletion",
                        #     #     props={"content": "AiCompletion content 123"},
                        #     # ),
                        # ],
                    )
                ),
            }
        if user_input == "/mtmeditor":
            logger.info("打开所见即所得编辑器")
            return {
                "uidelta": UiDelta(uiState=ChatBotUiState(isOpenMtmEditor=True)),
            }
        if user_input == "/dev_search":
            return {
                "uidelta": UiDelta(uiState=ChatBotUiState(isOpenSearchView=True)),
            }

        if user_input == "/start":
            a = state.get("uidelta")
            return {
                "messages": [
                    # new_user_message,
                    # ai_message,
                ],
                # "ui_messages": ui_messages,
                "uidelta": a,
            }
        return {}
