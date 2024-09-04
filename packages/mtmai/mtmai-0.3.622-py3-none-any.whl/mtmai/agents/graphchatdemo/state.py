import operator
from typing import Annotated

from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict

from mtmai.models.agent import AgentTaskBase

from .ctx import context

agent_name = "mtmaibot"


class UiChatItem(TypedDict, total=False):
    id: str | None = None
    component: str | None = None
    props: dict | None = None


class UiCommandsItem(TypedDict):
    name: str
    args: dict


class ExampleInputItem(TypedDict):
    title: str
    description: str
    content: str


class UIChatMessageItem(TypedDict):
    compType: str
    props: dict


class ChatBotUiState(TypedDict, total=False):
    agent: str | None = None
    isOpenAgentRagView: bool | None = False
    threadId: str | None = None
    agent_url_base: str | None = None
    graph_image_url: str | None = None
    isDev: bool | None = False
    isOpenRagUi: bool | None = False
    isOpenSearchView: bool | None = False
    isOpenMtmEditor: bool | None = False
    uichatitems: list[UIChatMessageItem] | None = None

    ui_messages: list[UiChatItem] | None = None
    example_input_items: list[ExampleInputItem]


class UiDelta(TypedDict):
    class Config:
        arbitrary_types_allowed = True

    commands: list[UiCommandsItem] | None = None
    uiState: ChatBotUiState | None = None


class MainState(TypedDict):
    # emails: list[dict] | None
    # action_required_emails: dict
    error: str | None = None
    user_input: str | None = None
    user_option: str | None = None
    user_id: str | None = None
    # messages: Annotated[Sequence[AnyMessage], operator.add]
    # messages: Annotated[Sequence[AnyMessage], operator.add_messages]
    messages: Annotated[list[AnyMessage], add_messages]

    context: context
    uidelta: UiDelta | None = None

    wait_editor_content: bool = False
    go_mtmeditor: bool = False
    uistate: ChatBotUiState | None = None  # 放弃
    ui_messages: Annotated[list[UiChatItem], operator.add]  # | None = None

    # 工具结果相关状态
    # web_search_results: str | None = None

    demo: AgentTaskBase | None = None
