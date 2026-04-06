CONFIG = {"configurable": {"thread_id": "conaigua_session"}}


class ChatRunner:

    def __init__(self, agent):
        self.agent = agent

    def run(self, user_input: str) -> str:
        buffer = ""

        for token, metadata in self.agent.stream(
            {"messages": [("user", user_input)]},
            config=CONFIG,
            stream_mode="messages"
        ):
            if token.content:
                buffer += token.content

        return buffer