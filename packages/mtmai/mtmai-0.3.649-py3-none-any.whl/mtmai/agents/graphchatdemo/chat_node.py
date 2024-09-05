import logging
from typing import Annotated

from langchain_core.messages import ChatMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState, tools_condition

from mtmai.agents.graphchatdemo.state import (
    MainState,
)
from mtmai.core.config import settings
from mtmai.models.agent import UiMessageBase, UiMessagePublic
from mtmai.tools.search_tools import search_tool

logger = logging.getLogger()

# primary_assistant_prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful customer support assistant for Swiss Airlines. "
#             " Use the provided tools to search for flights, company policies, and other information to assist the user's queries. "
#             " When searching, be persistent. Expand your query bounds if the first search returns no results. "
#             " If a search comes up empty, expand your search before giving up."
#             "\n\nCurrent user:\n<User>\n{user_info}\n</User>"
#             "\nCurrent time: {time}.",
#         ),
#         ("placeholder", "{messages}"),
#     ]
# ).partial(time=datetime.now())


def edge_chat_node(state: MainState):
    is_tools = tools_condition(state)
    if is_tools == "tools":
        return "chat_tools_node"
    if state.get("next"):
        return state.get("next")
    if state.get("go_mtmeditor"):
        return "mtmeditor"
    else:
        return "uidelta"


@tool
def call_supervisor(question: str):
    """Useful to call supervisor"""
    logger.info("调用 call_supervisor 工具 %s", question)
    return [f"我已经收到用户的问题, 正在后台处理 {question}"]


@tool(parse_docstring=False, response_format="content_and_artifact")
def open_document_editor(title: str, state: Annotated[dict, InjectedState]):
    """Useful to show document editor ui for user, 用户能够看到这个编辑器进行文章编辑"""
    return (
        "操作成功",
        {
            "artifaceType": "Document",
            "props": {
                "id": "fake-document-id",
                "title": "document-title1",
            },
        },
    )


@tool(parse_docstring=False, response_format="content_and_artifact")
def create_document(title: str, content: str, state: Annotated[dict, InjectedState]):
    """Useful to create new document for user"""
    return (
        "操作成功",
        {
            "artifaceType": "Document",
            "props": {
                "id": "fake-document-id",
                "title": title,
            },
        },
    )


@tool(parse_docstring=False, response_format="content_and_artifact")
def show_workflow_image():
    """Useful tool for displaying the internal workflow diagram of the current agent."""
    return (
        "Operation successful",
        {
            "artifaceType": "Image",
            "props": {
                "src": f"{settings.API_V1_STR}/agent/image/mtmaibot",
                "title": "流程图",
            },
        },
    )


@tool(parse_docstring=False, response_format="content_and_artifact")
def show_documents_admin_panel():
    """Useful to show document adminstrator ui, 显示知识库管理界面给用户"""
    return (
        '界面已经显示"打开知识库管理"按钮',
        {
            "ui_messages": [
                UiMessagePublic(
                    component="TriggerButton",
                    persist=False,
                    props={
                        "title": "点击编辑",
                        "children": {
                            "component": "DocsAdminPanel",
                            "props": {
                                # "title": title or "无标题文档",
                                # "content": content,
                            },
                        },
                    },
                )
            ],
        },
    )


chatbot_tools = [
    search_tool,
    call_supervisor,
    open_document_editor,
    create_document,
    show_documents_admin_panel,
    show_workflow_image,
]


class ChatNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: MainState, config: RunnableConfig):
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
        llm = self.runnable.bind_tools([*chatbot_tools])
        if messages[-1].type == "tool":
            ai_message = await llm.ainvoke(messages, config)

            artifaces_state = {}

            if messages[-1].artifact:
                artifaces_state = {"artifaces": [messages[-1].artifact]}

            ui_messages = [
                UiMessageBase(
                    component="AiCompletion", props={"content": ai_message.content}
                )
            ]
            return {
                **artifaces_state,
                "messages": [
                    ai_message,
                ],
                "ui_messages": ui_messages,
            }
        new_user_message = ChatMessage(role="user", content=state.get("user_input"))
        messages.append(new_user_message)
        ai_message = await llm.ainvoke(messages, config)

        ui_messages = [
            UiMessageBase(component="UserMessage", props={"content": user_input}),
        ]
        if ai_message.content:
            ui_messages.append(
                UiMessageBase(
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
                "ui_messages": [
                    UiMessageBase(
                        component="Image",
                        props={"src": f"{settings.API_V1_STR}/agent/image/mtmaibot"},
                    )
                ],
            }
        if user_input == "/start":
            a = state.get("uidelta")
            return {
                "messages": [],
                "uidelta": a,
            }
        return {}
