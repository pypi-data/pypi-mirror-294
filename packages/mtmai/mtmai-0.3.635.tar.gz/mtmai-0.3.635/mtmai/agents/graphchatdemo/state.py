from typing import Annotated

from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict

from mtmai.models.agent import UiMessageBase

from .ctx import context

agent_name = "mtmaibot"


class ChatBotUiState(TypedDict, total=False):
    agent: str | None = None
    isOpenAgentRagView: bool | None = False
    agent_url_base: str | None = None
    isDev: bool | None = False
    isOpenRagUi: bool | None = False
    isOpenSearchView: bool | None = False
    isOpenMtmEditor: bool | None = False
    ui_messages: list[UiMessageBase] | None = None


class UiDelta(TypedDict):
    class Config:
        arbitrary_types_allowed = True

    uiState: ChatBotUiState | None = None


class MainState(TypedDict):
    # emails: list[dict] | None
    # action_required_emails: dict
    error: str | None = None
    next: str | None = None
    user_input: str | None = None
    user_option: str | None = None
    wait_human: bool | None = False
    # user_id: str | None = None
    # messages: Annotated[Sequence[AnyMessage], operator.add]
    # messages: Annotated[Sequence[AnyMessage], operator.add_messages]
    messages: Annotated[list[AnyMessage], add_messages]

    context: context
    uidelta: UiDelta | None = None

    wait_editor_content: bool = False
    go_mtmeditor: bool = False
    uistate: ChatBotUiState | None = None  # 放弃
    ui_messages: list[UiMessageBase]  # | None = None
    # demo: AgentTaskBase | None = None
