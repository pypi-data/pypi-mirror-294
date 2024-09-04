import logging

from langchain_core.runnables import RunnableConfig

from mtmai.agents.graphchatdemo.state import (
    MainState,
)

logger = logging.getLogger()


class HumanNode:
    def __init__(self):
        pass

    async def __call__(self, state: MainState, config: RunnableConfig):
        # ui_messages = state.get("ui_messages")
        # uidelta_update = state.get("uidelta")
        # return {
        #     "uidelta": uidelta_update,
        #     "ui_messages": ui_messages,
        # }
        logger.info("到达 human_node")
