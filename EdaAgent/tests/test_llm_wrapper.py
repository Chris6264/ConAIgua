import pytest
from unittest.mock import patch, MagicMock


def test_build_llm_groq(mock_config):
    with patch("conaigua.utils.config_manager.ConfigManager.load_config") as mock_loader:
        mock_loader.return_value = mock_config

        with patch("conaigua.eda_agent.config.llm_wrapper.ChatGroq") as mock:
            mock.return_value = MagicMock()

            from conaigua.eda_agent.config.llm_wrapper import build_llm
            build_llm()

            mock.assert_called_once()


def test_build_llm_openai(mock_config):
    mock_config["llm"]["provider"] = "openai"
    mock_config["llm"]["model"] = "gpt-4o"

    with patch("conaigua.utils.config_manager.ConfigManager.load_config") as mock_loader:
        mock_loader.return_value = mock_config

        with patch("conaigua.eda_agent.config.llm_wrapper.ChatOpenAI") as mock:
            mock.return_value = MagicMock()

            from conaigua.eda_agent.config.llm_wrapper import build_llm
            build_llm()

            mock.assert_called_once()


def test_build_llm_provider_invalido(mock_config):
    mock_config["llm"]["provider"] = "invalido"

    with patch("conaigua.utils.config_manager.ConfigManager.load_config") as mock_loader:
        mock_loader.return_value = mock_config

        from conaigua.eda_agent.config.llm_wrapper import build_llm

        with pytest.raises(ValueError):
            build_llm()


def test_llm_defaults(mock_config):
    with patch("conaigua.utils.config_manager.ConfigManager.load_config") as mock_loader:
        mock_loader.return_value = mock_config

        with patch("conaigua.eda_agent.config.llm_wrapper.ChatGroq") as mock:
            mock.return_value = MagicMock()

            from conaigua.eda_agent.config.llm_wrapper import build_llm
            build_llm()

            _, kwargs = mock.call_args

            assert kwargs["temperature"] == 0
            assert kwargs["max_tokens"] == 1024