import logging

from langgraph.graph import END, StateGraph

from mtmai.agents.graphchatdemo.chat_node import ChatNode, edge_chat_node
from mtmai.agents.graphchatdemo.entry_node import EntryNode, edge_entry
from mtmai.agents.graphchatdemo.graphutils import create_tool_node_with_fallback
from mtmai.agents.graphchatdemo.mtmeditor_node import MtmEditorNode, edge_mtmeditor
from mtmai.agents.graphchatdemo.nodes import Nodes
from mtmai.agents.graphchatdemo.sub_image.graph_image import SubGraphText2Image
from mtmai.agents.graphchatdemo.ui_node import UiNode
from mtmai.mtlibs.aiutils import lcllm_openai_chat

from .state import MainState
from .tools import default_tools

logger = logging.getLogger()


class GraphChatDemoAgent:
    def build_flow(self):
        nodes = Nodes()
        llm = lcllm_openai_chat("")
        sub_text2image_graph = SubGraphText2Image().build_flow()
        wf = StateGraph(MainState)
        wf.add_node("entry", EntryNode(llm))
        wf.add_node("chat", ChatNode(llm))
        wf.add_node("tools", create_tool_node_with_fallback(default_tools))
        wf.add_node("uidelta_node", UiNode(llm))
        wf.add_node("finnal_node", nodes.finnal_node)

        wf.set_entry_point("entry")
        wf.add_conditional_edges(
            "entry",
            edge_entry,
            {
                "chat": "chat",
                "end": END,
            },
        )

        wf.add_edge("uidelta_node", "chat")
        wf.add_edge("tools", "chat")
        wf.add_conditional_edges(
            "chat",
            edge_chat_node,
            {
                "tools": "tools",
                "mtmeditor": "mtmeditor",
                "uidelta": "uidelta_node",
                "end": END,
            },
        )

        wf.add_node("mtmeditor", MtmEditorNode(llm))
        wf.add_conditional_edges(
            "mtmeditor",
            edge_mtmeditor,
            {
                "uidelta": "uidelta_node",
                "finnal": "finnal_node",
            },
        )

        return wf

    # async def chat(
    #     self,
    #     user_id: str,
    #     prompt: str | None = None,
    #     thread_id: str | None = None,
    #     option=None,
    # ):
    #     async with AsyncPostgresSaver.from_conn_string(
    #         settings.DATABASE_URL
    #     ) as checkpointer:
    #         app = self.build_flow().compile(
    #             checkpointer=checkpointer,
    #             # interrupt_before=["uidelta_node"]
    #             interrupt_after=["uidelta_node"],
    #         )

    #         is_new_thread = not thread_id
    #         if not thread_id:
    #             thread_id = mtutils.gen_orm_id_key()

    #         thread: RunnableConfig = {
    #             "configurable": {"thread_id": thread_id, "user_id": user_id}
    #         }

    #         # state1 = await app.aget_state(thread)
    #         inputs = None
    #         if is_new_thread:
    #             # 全新状态的情况
    #             logger.info("新对话 %s", thread_id)
    #             inputs = {
    #                 "user_id": user_id,
    #                 "user_input": prompt,
    #                 "user_option": option,
    #                 # "config": DemoAgentConfig(
    #                 #     name=self.name,
    #                 # ),
    #             }
    #         else:
    #             await app.aupdate_state(
    #                 thread,
    #                 {
    #                     "user_input": prompt,
    #                     "user_option": option,
    #                     "uidelta": None,
    #                 },
    #                 as_node="uidelta_node",
    #             )
    #         async for event in app.astream_events(
    #             inputs,
    #             version="v2",
    #             config=thread,
    #         ):
    #             kind = event["event"]
    #             node_name = event["name"]
    #             data = event["data"]
    #             # tags = event.get("tags", [])
    #             logger.info("%s:node: %s", kind, node_name)
    #             if kind == "on_chat_model_stream":
    #                 content = data["chunk"].content
    #                 if content:
    #                     print(content, end="", flush=True)
    #                     yield aisdk.text(content)

    #                 if event["metadata"].get("langgraph_node") == "final":
    #                     logger.info("终结节点")

    #             if kind == "on_chain_stream":
    #                 if data and (node_name == "uidelta_node" or node_name == "tools"):
    #                     chunk_data = data.get("chunk", {})
    #                     picked_data = {
    #                         key: chunk_data[key]
    #                         for key in ["uidelta"]
    #                         if key in chunk_data
    #                     }

    #                     if picked_data:
    #                         yield aisdk.data(picked_data)
    #             if kind == "on_chain_end" and node_name == "LangGraph":
    #                 # yield aisdk.data(jsonable_encoder(data))
    #                 final_messages = event["data"]["output"]["messages"]
    #                 for message in final_messages:
    #                     message.pretty_print()
    #                 logger.info("中止节点")

    #         yield aisdk.finish()
