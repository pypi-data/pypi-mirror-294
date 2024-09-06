import logging

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from opentelemetry import trace
from pydantic import BaseModel

from mtmai.agents.agent_api import get_agent_by_name_v3
from mtmai.api.deps import OptionalUserDep, SessionDep
from mtmai.mtlibs import aisdk

router = APIRouter()
logger = logging.getLogger()
tracer = trace.get_tracer_provider().get_tracer(__name__)


class ChatRequest(BaseModel):
    """前端 vercel ai sdk 客户端提交过来的聊天消息"""

    messages: any

    class Config:
        arbitrary_types_allowed = True


async def agent_chat_stream(
    *,
    user_id: str,
    agent_name: str | None = None,
    thread_id: str | None = None,
    prompt: str | None = None,
    option=None,
):
    agent = get_agent_by_name_v3(agent_name)
    if not agent:
        yield aisdk.text(f"error missing agent: {agent_name}")
        yield aisdk.finish()
        return

    agent_inst = agent()
    async for chunck in agent_inst.chat(
        user_id=user_id,
        prompt=prompt,
        option=option,
        thread_id=thread_id,
    ):
        yield chunck


# @traceable
@router.post("/chat/completions")
async def chat_completions(db: SessionDep, user: OptionalUserDep, request: Request):
    agent_name = request.headers.get("X-Ai-Agent")
    thread_id = request.headers.get("X-Thread-Id")
    payload = await request.json()
    response = response = StreamingResponse(
        agent_chat_stream(
            # db=db,
            agent_name=agent_name,
            user_id=user.id,
            prompt=payload.get("prompt"),
            option=payload.get("option"),
            thread_id=thread_id,
        ),
        media_type="text/event-stream",
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response
