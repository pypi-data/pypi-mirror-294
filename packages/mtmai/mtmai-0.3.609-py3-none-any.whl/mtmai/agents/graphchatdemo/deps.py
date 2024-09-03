from typing import Annotated

from fastapi import Depends
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph.state import CompiledStateGraph

from mtmai.agents.graphchatdemo.graph import GraphChatDemoAgent
from mtmai.core.config import settings


async def get_checkpointer():
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
    from psycopg_pool import AsyncConnectionPool

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    poll = AsyncConnectionPool(
        conninfo=settings.DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    checkpointer = AsyncPostgresSaver(poll)
    yield checkpointer


CheckPointerDep = Annotated[AsyncPostgresSaver, Depends(get_checkpointer)]


async def get_graph(checkpointer: CheckPointerDep):
    agent_inst = GraphChatDemoAgent()
    app = agent_inst.build_flow().compile(
        checkpointer=checkpointer,
        interrupt_after=["uidelta_node"],
    )
    yield app


GraphAppDep = Annotated[CompiledStateGraph, Depends(get_graph)]
