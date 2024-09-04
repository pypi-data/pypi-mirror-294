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
        # ui_messages = state.get("ui_messages")

        # # TODO: 数据库操作 可以使用另外的线程或节点并发执行
        # for uim in ui_messages:
        #     db_ui_message2 = UiMessage(
        #         thread_id=thread_id,
        #         user_id=user_id,
        #         component=uim.get("component"),
        #         props=uim.get("props"),
        #     )
        #     session.add(db_ui_message2)
        #     session.commit()

        # # 跳过前端已经乐观更新的组件
        # skip_components = ["UserMessage", "AiCompletion"]
        # filterd_components = [
        #     x for x in ui_messages if x.get("component") not in skip_components
        # ]
        return {
            "wait_human": True,
            # "uidelta": state.get("uidelta"),
            # "ui_messages": filterd_components,
        }
