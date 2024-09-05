import logging

from langgraph.graph import END, StateGraph

from mtmai.agents.graphchatdemo.chat_node import ChatNode, chatbot_tools, edge_chat_node
from mtmai.agents.graphchatdemo.entry_node import EntryNode, edge_entry
from mtmai.agents.graphchatdemo.graphutils import create_tool_node_with_fallback
from mtmai.agents.graphchatdemo.mtmeditor_node import MtmEditorNode, edge_mtmeditor
from mtmai.agents.graphchatdemo.node_human import HumanNode, edge_human_node
from mtmai.agents.graphchatdemo.node_supervisor import SupervisorNode
from mtmai.agents.graphchatdemo.nodes import Nodes
from mtmai.agents.graphchatdemo.sub_image.graph_image import SubGraphText2Image
from mtmai.agents.graphchatdemo.ui_node import UiNode, edge_uinode
from mtmai.llm.llm import get_llm_chatbot_default

from .state import MainState

logger = logging.getLogger()


class GraphChatDemoAgent:
    def build_flow(self):
        nodes = Nodes()
        llm = get_llm_chatbot_default()
        sub_text2image_graph = SubGraphText2Image().build_flow()
        wf = StateGraph(MainState)
        wf.add_node("entry_node", EntryNode(llm))
        wf.add_node("chat_node", ChatNode(llm))
        wf.add_node("chat_tools_node", create_tool_node_with_fallback(chatbot_tools))
        wf.add_node("uidelta_node", UiNode(llm))
        wf.add_node("finnal_node", nodes.finnal_node)
        wf.add_node("supervisor_node", SupervisorNode(llm))

        wf.set_entry_point("entry_node")
        wf.add_conditional_edges(
            "entry_node",
            edge_entry,
            {
                "chat_node": "chat_node",
                "end": END,
            },
        )

        wf.add_conditional_edges(
            "uidelta_node",
            edge_uinode,
            {
                "chat_node": "chat_node",
                "human_node": "human_node",
            },
        )
        wf.add_edge("chat_tools_node", "chat_node")
        wf.add_conditional_edges(
            "chat_node",
            edge_chat_node,
            {
                "chat_tools_node": "chat_tools_node",
                "mtmeditor": "mtmeditor",
                "uidelta": "uidelta_node",
                "supervisor": "supervisor_node",
                "human": "human_node",
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

        wf.add_node("human_node", HumanNode())
        wf.add_conditional_edges(
            "human_node",
            edge_human_node,
            {
                "chat_node": "chat_node",
            },
        )

        return wf
