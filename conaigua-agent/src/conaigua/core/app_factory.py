from conaigua.eda_agent.config.agent_setup import build_agent
from conaigua.eda_agent.runner.chat_runner import ChatRunner
from conaigua.eda_agent.runner.response_handler import ResponseHandler


def build_app(console):
    agent = build_agent()
    runner = ChatRunner(agent)
    handler = ResponseHandler(console)
    return runner, handler