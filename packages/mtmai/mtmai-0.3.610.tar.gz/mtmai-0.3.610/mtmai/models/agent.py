from datetime import datetime
from typing import TYPE_CHECKING

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from mtmai.mtlibs import mtutils

if TYPE_CHECKING:
    import mtmai


class AgentTaskBase(SQLModel):
    title: str | None = Field(default="")
    description: str | None = Field(default="")
    path: str | None = Field(default="")
    share_path: str | None = Field(default="")


class AgentTask(AgentTaskBase, table=True):
    """对应 langgraph 一个工作流的运行"""

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    thread_id: str
    user_id: str = Field(default=None, foreign_key="user.id")
    user: "mtmai.models.models.User" = Relationship(back_populates="agenttasks")

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    output: str | None = Field(default="")
    config: RunnableConfig = Field(sa_column=Column(JSON))


# class AgentChatConfig(BaseModel):
#     chat_endpoint: str | None = None


class AgentMeta(BaseModel):
    id: str
    name: str
    base_url: str
    chat_url: str | None = None
    can_chat: bool = (False,)
    agent_type: str | None = None
    graph_image: str | None = None
    label: str | None = None
    description: str | None = None
    # chat_agent_config: AgentChatConfig | None = None


class UiMessageBase(SQLModel):
    class Config:
        # Needed for Column(JSON)
        arbitrary_types_allowed = True

    role: str
    component: str = Field(default=None, max_length=64, min_length=1)
    props: dict = Field(default_factory=dict, sa_column=Column(JSON))
    thread_id: str = Field(default=None, max_length=255, min_length=10)


class UiMessage(UiMessageBase, table=True):
    # class Config:
    #     # Needed for Column(JSON)
    #     arbitrary_types_allowed = True

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    user_id: str = Field(default=None, foreign_key="user.id")
    user: "mtmai.models.models.User" = Relationship(back_populates="uimessages")

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
