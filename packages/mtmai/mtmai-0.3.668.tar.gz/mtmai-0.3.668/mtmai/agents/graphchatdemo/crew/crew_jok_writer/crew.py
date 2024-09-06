from crewai import Crew
from langchain_core.runnables import Runnable

from mtmai.llm.llm import get_llm_chatbot_default

from .agents import JokAgents
from .tasks import EmailFilterTasks


class JokeCrew:
    def __init__(self, runnable: Runnable):
        agents = JokAgents()
        # self.filter_agent = agents.email_filter_agent()
        self.joke_writer_agent = agents.joke_writer_agent()
        # self.writer_agent = agents.email_response_writer()
        self.runnable = runnable

    async def kickoff(self, state):
        tasks = EmailFilterTasks()
        emails = ["a@a.com"]
        llm = get_llm_chatbot_default()
        crew = Crew(
            agents=[
                self.joke_writer_agent,
                # self.action_agent,
                # self.writer_agent,
            ],
            tasks=[
                tasks.filter_emails_task(
                    self.joke_writer_agent, self._format_emails(emails)
                ),
                # tasks.action_required_emails_task(self.action_agent),
                # tasks.draft_responses_task(self.writer_agent),
            ],
            verbose=True,
            manager_llm=llm,
            function_calling_llm=llm,
            planning_llm=llm,
        )
        result = await crew.kickoff_async()
        return {**state, "action_required_emails": result}

    def _format_emails(self, emails):
        # emails_string = []
        # for email in emails:
        #     print(email)
        #     arr = [
        #         f"ID: {email['id']}",
        #         f"- Thread ID: {email['threadId']}",
        #         f"- Snippet: {email['snippet']}",
        #         f"- From: {email['sender']}",
        #         "--------",
        #     ]
        #     emails_string.append("\n".join(arr))
        # return "\n".join(emails_string)
        return ["ssssssss", "task22222", "task3333"]
