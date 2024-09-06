from typing import Literal

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig
from pydantic import BaseModel

from mtmai.agents.graphchatdemo.state import MainState

members = ["Researcher", "Programmer", "HumanChat"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)
# Our team supervisor is an LLM node. It just picks the next agent to process
# and decides when the work is completed
options = [*members]


class RouteResponse(BaseModel):
    next: Literal[*options]


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next?"
            " Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))


def edge_supervisor(state: MainState):
    next_to = state.get("next")
    if next_to:
        return next_to
    return "__end__"


class SupervisorNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: MainState, config: RunnableConfig):
        supervisor_chain = prompt | self.runnable.with_structured_output(RouteResponse)
        result = supervisor_chain.invoke(state)
        return result
