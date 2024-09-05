import logging

from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.graphchatdemo.state import (
    MainState,
)

logger = logging.getLogger()


def edge_uinode(state: MainState):
    if state.get("wait_human"):
        return "human_node"
    return "chat_node"


class UiNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: MainState, config: RunnableConfig):
        """工作流内 ui_messages (对应客户端组件) 的增量变化同步到数据库中"""
        # thread_id = config.get("configurable").get("thread_id")
        # user_id = config.get("configurable").get("user_id")
        # session = state.get("context").session
        return {
            "wait_human": True,
        }
