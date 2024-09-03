import logging

from fastapi import APIRouter, Header, Response
from fastapi.responses import StreamingResponse
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel
from sqlmodel import Session, SQLModel, select

from mtmai.api.deps import GraphAppDep, OptionalUserDep, SessionDep
from mtmai.core.config import settings
from mtmai.models.agent import AgentMeta
from mtmai.models.chat import ChatInput
from mtmai.models.models import Agent
from mtmai.mtlibs import aisdk, mtutils

router = APIRouter()

logger = logging.getLogger()
graphs: dict[str, CompiledStateGraph] = {}


async def get_agent_from_headers(chat_agent: str = Header(None)):
    return chat_agent


def ensure_thread_id(input: ChatInput):
    if not input.config:
        input.config = {}

    if not input.config.get("configurable"):
        input.config["configurable"] = {}
    if not input.config["configurable"].get("thread_id"):
        input.config["configurable"]["thread_id"] = mtutils.gen_orm_id_key()
    if not input.config["configurable"].get("chat_id"):
        input.config["configurable"]["chat_id"] = input.id
    return input


def get_agent_by_id(db: Session, agent_id: str):
    return db.exec(select(Agent).where(Agent.id == agent_id)).one()


agent_list = []


def register_agent(agent_obj):
    agent_list.append(agent_obj)


def init_agent_list():
    from mtmai.agents.simple_chat import SimpleChatAgent

    register_agent(SimpleChatAgent)


init_agent_list()


def get_agent_by_name_v2(agent_name: str):
    if agent_name == "simplechat":
        from mtmai.agents.simple_chat import SimpleChatAgent

        return SimpleChatAgent
    if agent_name == "joke":
        from mtmai.agents.joke_agent import JokeAgent

        return JokeAgent

    if agent_name == "graphchatdemo":
        from mtmai.agents.graphchatdemo.graph import GraphChatDemoAgent

        return GraphChatDemoAgent

    return None


agents = {}


def get_agent_by_name_v3(agent_name: str):
    global agents
    a = agents.get(agent_name)
    if not a:
        b = get_agent_by_name_v2(agent_name)
        # agent_inst = b()
        agents[agent_name] = b
    return agents.get(agent_name)


class AgentsPublic(SQLModel):
    data: list[AgentMeta]
    count: int


all_agents = [
    AgentMeta(
        id="mtmaibot",
        name="mtmaibot",
        label="AI聊天",
        base_url=settings.API_V1_STR + "/mtmaibot",
        description="基于 graph 的综合智能体(开发版)",
        can_chat=True,
        agent_type="chat",
        # chat_agent_config=AgentChatConfig(),
        is_dev=True,
    ),
    AgentMeta(
        id="mteditor",
        name="mteditor",
        label="AI所见即所得编辑器",
        base_url=settings.API_V1_STR + "/mteditor",
        description="演示版",
        # chat_url=settings.API_V1_STR + "/mteditor/chat",
        can_chat=False,
        agent_type="mtmeditor",
        graph_image=settings.API_V1_STR + "/mteditor/image",
    ),
]


@router.get(
    "",
    summary="获取 Agent 列表",
    description=(
        "此端点用于获取 agent 列表。支持分页功能"
        "可以通过 `skip` 和 `limit` 参数控制返回的 agent 数量。"
    ),
    response_description="返回包含所有 agent 的列表及总数。",
    response_model=AgentsPublic,
    responses={
        200: {
            "description": "成功返回 agent 列表",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {"name": "agent1", "status": "active"},
                            {"name": "agent2", "status": "inactive"},
                        ],
                        "count": 2,
                    }
                }
            },
        },
        401: {"description": "未经授权的请求"},
        500: {"description": "服务器内部错误"},
    },
)
def items(
    # db: SessionDep,
    user: OptionalUserDep,
    skip: int = 0,
    limit: int = 100,
):
    return AgentsPublic(data=all_agents, count=len(all_agents))


@router.get("/{agent_id}", response_model=AgentMeta | None)
def get_item(db: SessionDep, user: OptionalUserDep, agent_id: str):
    for agent in all_agents:
        if agent.id == agent_id:
            return agent
    return None


# @router.get(
#     "/{agent_id}/image",
#     summary="获取工作流图像",
#     description="此端点通过给定的 agent ID，生成工作流的图像并返回 PNG 格式的数据。",
#     response_description="返回 PNG 格式的工作流图像。",
#     responses={
#         200: {"content": {"image/png": {}}},
#         404: {"description": "Agent 未找到"},
#     },
# )


@router.get("/graph_image")
async def graph_image(user: OptionalUserDep, graphapp: GraphAppDep):
    # agent_inst = GraphChatDemoAgent()

    image_data = graphapp.get_graph(xray=1).draw_mermaid_png()
    return Response(content=image_data, media_type="image/png")


# async def get_workflow_image(user: OptionalUserDep, agent_id: str):
#     agent = get_agent_by_name_v3(agent_id)
#     if not agent:
#         raise HTTPException(status_code=404, detail="Agent 未找到")

#     app = (
#         agent()
#         .build_flow()
#         .compile(
#             # checkpointer=checkpointer,
#             # interrupt_before=["uidelta_node"]
#             # interrupt_after=["uidelta_node"],
#         )
#     )

#     image_data = app.get_graph(xray=1).draw_mermaid_png()
#     return Response(content=image_data, media_type="image/png")


class AgentStateRequest(BaseModel):
    agent_id: str | None = None
    thread_id: str


@router.post(
    "/state",
    summary="获取工作流状态",
    description="",
    response_description="返回工作流当前完整状态数据",
)
async def state(req: AgentStateRequest, user: OptionalUserDep, graphapp: GraphAppDep):
    thread: RunnableConfig = {"configurable": {"thread_id": req.thread_id}}
    state = await graphapp.aget_state(thread)
    return state


# class ChatBotUiStatePublic(BaseModel):
#     ui_state: ChatBotUiState


# @router.get(
#     "/{agent_id}/{thread_id}/uistate",
#     summary="获取 chat bot UiState",
#     description="",
#     response_description="前端 聊天机器人 UI 状态（UI初始化时用到）",
#     response_model=ChatBotUiStatePublic,
# )
# async def get_ui_state(user: OptionalUserDep, agent_id: str, thread_id: str):
#     agent = get_agent_by_name_v3(agent_id)
#     if not agent:
#         raise HTTPException(status_code=404, detail="Agent 未找到")

#     thread: RunnableConfig = {"configurable": {"thread_id": thread_id}}
#     state = agent.app.get_state(thread)
#     return state


# class AgentMessageItemPublic(MtmChatMessageBase):
#     agent_id: str


# class AgentMessagePublic(SQLModel):
#     data: list[AgentMessageItemPublic]
#     count: int


# @router.get("/{agent_id}/messages", response_model=AgentMessagePublic)
# async def messages(
#     *,
#     session: Session = Depends(get_session),
#     offset: int = 0,
#     limit: int = Query(default=100, le=100),
#     user: OptionalUserDep,
#     agent_id: str,
# ):
#     if not user:
#         return None

#     count_statement = (
#         select(func.count())
#         .select_from(MtmChatMessage)
#         .where(MtmChatMessage.owner_id == user.id)
#     )
#     count = session.exec(count_statement).one()
#     items = get_conversation_messages(
#         db=session, offset=offset, limit=limit, conversation_id=agent_id
#     )
#     return AgentMessagePublic(data=items, count=count)


async def agent_event_stream(
    *,
    graph: CompiledStateGraph,
    inputs,
    thread: RunnableConfig,
):
    async for event in graph.astream_events(
        inputs,
        version="v2",
        config=thread,
    ):
        kind = event["event"]
        node_name = event["name"]
        data = event["data"]
        # tags = event.get("tags", [])
        logger.info("%s:node: %s", kind, node_name)
        if kind == "on_chat_model_stream":
            content = data["chunk"].content
            if content:
                print(content, end="", flush=True)
                yield aisdk.text(content)

            if event["metadata"].get("langgraph_node") == "final":
                logger.info("终结节点")

        if kind == "on_chain_stream":
            if data and (node_name == "uidelta_node" or node_name == "tools"):
                chunk_data = data.get("chunk", {})
                picked_data = {
                    key: chunk_data[key] for key in ["uidelta"] if key in chunk_data
                }

                if picked_data:
                    yield aisdk.data(picked_data)
        if kind == "on_chain_end" and node_name == "LangGraph":
            # yield aisdk.data(jsonable_encoder(data))
            final_messages = event["data"]["output"]["messages"]
            for message in final_messages:
                message.pretty_print()
            logger.info("中止节点")

    yield aisdk.finish()


class CompletinRequest(BaseModel):
    thread_id: str | None = None
    prompt: str
    option: str | None = None


@router.post("/completions")
async def completions(
    user: OptionalUserDep, graphapp: GraphAppDep, req: CompletinRequest
):
    thread_id = req.thread_id
    if not thread_id:
        thread_id = mtutils.gen_orm_id_key()
    thread: RunnableConfig = {
        "configurable": {"thread_id": thread_id, "user_id": user.id}
    }

    response = response = StreamingResponse(
        agent_event_stream(
            graph=graphapp,
            inputs={
                "user_id": user.id,
                "user_input": req.prompt,
                "user_option": req.option,
            },
            thread=thread,
        ),
        media_type="text/event-stream",
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response
