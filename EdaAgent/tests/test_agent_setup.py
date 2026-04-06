from unittest.mock import patch, MagicMock


def test_build_agent():
    with patch("conaigua.eda_agent.config.agent_setup.build_llm") as mock_llm:
        mock_llm.return_value = MagicMock()

        from conaigua.eda_agent.config.agent_setup import build_agent
        agent = build_agent()

        assert agent is not None


def test_build_agent_llama_log():
    with patch("conaigua.eda_agent.config.agent_setup.build_llm") as mock_llm:
        with patch("conaigua.eda_agent.config.agent_setup.log_agent_start") as mock_log:

            mock_llm.return_value = MagicMock()

            from conaigua.eda_agent.config.agent_setup import build_agent
            build_agent()

            mock_log.assert_called_once()


def test_tools_count():
    from conaigua.eda_agent.config.agent_setup import TOOLS
    assert len(TOOLS) == 7