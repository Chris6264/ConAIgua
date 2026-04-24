from unittest.mock import patch, MagicMock

def test_build_agent():
    with patch("conaigua.eda_agent.config.agent_setup.build_llm") as mock_llm:
        mock_llm.return_value = MagicMock()

        from conaigua.eda_agent.config.agent_setup import build_agent
        agent = build_agent()

        assert agent is not None

def test_tools_count():
    from conaigua.eda_agent.config.agent_setup import TOOLS
    assert len(TOOLS) == 8