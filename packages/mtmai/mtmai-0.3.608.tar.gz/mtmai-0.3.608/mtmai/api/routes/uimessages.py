import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import func, select

from mtmai.api.deps import CurrentUser, SessionDep
from mtmai.models.agent import UiMessage, UiMessageBase

router = APIRouter()
logger = logging.getLogger()
# tracer = trace.get_tracer_p


class UiMessagesRequest(BaseModel):
    thread_id: str | None = None


class UiMessagesItem(UiMessageBase):
    id: str


class UiMessagesResponse(BaseModel):
    data: list[UiMessagesItem]
    count: int


@router.get("", response_model=UiMessagesResponse)
async def items(
    session: SessionDep, user: CurrentUser, skip: int = 0, limit: int = 100
):
    if not user:
        raise Exception("require user")
    if user.is_superuser:
        count_statement = select(func.count()).select_from(UiMessage)
        count = session.exec(count_statement).one()
        statement = select(UiMessage).offset(skip).limit(limit)
        items = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(UiMessage)
            .where(UiMessage.user_id == user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(UiMessage)
            .where(UiMessage.owner_id == user.id)
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).all()

    return UiMessagesResponse(data=items, count=count)


class UiMessagesCreate(UiMessageBase):
    pass


@router.post("", response_model=UiMessagesItem)
def create_item(
    *, session: SessionDep, user: CurrentUser, item_in: UiMessagesCreate
) -> Any:
    """
    Create new item.
    """
    item = UiMessage.model_validate(item_in, update={"user_id": user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
