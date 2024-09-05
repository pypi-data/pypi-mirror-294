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
        logger.info("到达 human_node")
