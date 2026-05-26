
class ChatRunner:
    def __init__(self, agent):
        self.agent = agent

    def stream(self, user_input: str, config: dict | None = None):
        """
        Stream real token por token.
        """
        for token, metadata in self.agent.stream(
            {"messages": [("user", user_input)]},
            config=config,
            stream_mode="messages",
        ):
            if token.content:
                yield token.content

    def run(self, user_input: str, config: dict | None = None) -> str:
        """
        Modo no-stream: junta todos los tokens y devuelve texto completo.
        """
        buffer = ""

        for chunk in self.stream(user_input, config=config):
            buffer += chunk

        return buffer