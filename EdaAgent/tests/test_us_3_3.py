import os
import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

load_dotenv()

# ── LLM Wrapper ──────────────────────────────────

def test_modelos_groq_existen():
    from scripts.eda_agent.config.llm_wrapper import MODELOS_GROQ
    assert "rapido" in MODELOS_GROQ
    assert "balanceado" in MODELOS_GROQ
    assert "razonamiento" in MODELOS_GROQ

def test_modelos_openai_existen():
    from scripts.eda_agent.config.llm_wrapper import MODELOS_OPENAI
    assert "rapido" in MODELOS_OPENAI
    assert "balanceado" in MODELOS_OPENAI

def test_modelos_anthropic_existen():
    from scripts.eda_agent.config.llm_wrapper import MODELOS_ANTHROPIC
    assert "rapido" in MODELOS_ANTHROPIC
    assert "balanceado" in MODELOS_ANTHROPIC

def test_modelos_google_existen():
    from scripts.eda_agent.config.llm_wrapper import MODELOS_GOOGLE
    assert "rapido" in MODELOS_GOOGLE
    assert "balanceado" in MODELOS_GOOGLE

def test_build_llm_groq():
    os.environ["LLM_PROVIDER"] = "groq"
    from scripts.eda_agent.config.llm_wrapper import build_llm, MODELOS_GROQ
    with patch("scripts.eda_agent.config.llm_wrapper.ChatGroq") as mock:
        mock.return_value = MagicMock(model_name=MODELOS_GROQ["rapido"])
        build_llm(modelo="rapido")
        mock.assert_called_once()

def test_build_llm_openai():
    os.environ["LLM_PROVIDER"] = "openai"
    from scripts.eda_agent.config.llm_wrapper import build_llm
    with patch("scripts.eda_agent.config.llm_wrapper.ChatOpenAI") as mock:
        mock.return_value = MagicMock()
        build_llm(modelo="rapido")
        mock.assert_called_once()
    os.environ["LLM_PROVIDER"] = "groq"

def test_build_llm_anthropic():
    os.environ["LLM_PROVIDER"] = "anthropic"
    from scripts.eda_agent.config.llm_wrapper import build_llm
    with patch("scripts.eda_agent.config.llm_wrapper.ChatAnthropic") as mock:
        mock.return_value = MagicMock()
        build_llm(modelo="rapido")
        mock.assert_called_once()
    os.environ["LLM_PROVIDER"] = "groq"

def test_build_llm_google():
    os.environ["LLM_PROVIDER"] = "google"
    from scripts.eda_agent.config.llm_wrapper import build_llm
    with patch("scripts.eda_agent.config.llm_wrapper.ChatGoogleGenerativeAI") as mock:
        mock.return_value = MagicMock()
        build_llm(modelo="rapido")
        mock.assert_called_once()
    os.environ["LLM_PROVIDER"] = "groq"

def test_build_llm_provider_invalido():
    os.environ["LLM_PROVIDER"] = "invalido"
    from scripts.eda_agent.config.llm_wrapper import build_llm
    with pytest.raises(ValueError):
        build_llm()
    os.environ["LLM_PROVIDER"] = "groq"

def test_llm_wrapper_temperatura_default():
    from scripts.eda_agent.config.llm_wrapper import build_llm
    with patch("scripts.eda_agent.config.llm_wrapper.ChatGroq") as mock:
        mock.return_value = MagicMock()
        build_llm()
        _, kwargs = mock.call_args
        assert kwargs["temperature"] == 0

def test_llm_wrapper_max_tokens_default():
    from scripts.eda_agent.config.llm_wrapper import build_llm
    with patch("scripts.eda_agent.config.llm_wrapper.ChatGroq") as mock:
        mock.return_value = MagicMock()
        build_llm()
        _, kwargs = mock.call_args
        assert kwargs["max_tokens"] == 1024

def test_llm_wrapper_modelo_default_es_razonamiento():
    from scripts.eda_agent.config.llm_wrapper import build_llm, MODELOS_GROQ
    with patch("scripts.eda_agent.config.llm_wrapper.ChatGroq") as mock:
        mock.return_value = MagicMock()
        build_llm()
        _, kwargs = mock.call_args
        assert kwargs["model"] == MODELOS_GROQ["razonamiento"]

# ── Checkpointer ─────────────────────────────────

def test_memory_saver():
    from langgraph.checkpoint.memory import InMemorySaver
    checkpointer = InMemorySaver()
    assert checkpointer is not None

# ── Agent setup ──────────────────────────────────

def test_tools_count():
    from scripts.eda_agent.config.agent_setup import TOOLS
    assert len(TOOLS) == 7

def test_tools_tienen_docstring():
    from scripts.eda_agent.config.agent_setup import TOOLS
    for tool in TOOLS:
        assert tool.description, f"Tool '{tool.name}' no tiene docstring"

def test_tools_tienen_nombre():
    from scripts.eda_agent.config.agent_setup import TOOLS
    for tool in TOOLS:
        assert tool.name, f"Una tool no tiene nombre"

def test_tools_nombres_unicos():
    from scripts.eda_agent.config.agent_setup import TOOLS
    nombres = [tool.name for tool in TOOLS]
    assert len(nombres) == len(set(nombres)), "Hay tools con nombres duplicados"

def test_system_prompt():
    from scripts.eda_agent.config.agent_setup import SYSTEM_PROMPT
    assert "ConAIgua" in SYSTEM_PROMPT
    assert "CONAGUA" in SYSTEM_PROMPT
    assert "Límites estrictos" in SYSTEM_PROMPT

def test_system_prompt_tiene_capacidades():
    from scripts.eda_agent.config.agent_setup import SYSTEM_PROMPT
    assert "Capacidades" in SYSTEM_PROMPT

def test_system_prompt_tiene_variables():
    from scripts.eda_agent.config.agent_setup import SYSTEM_PROMPT
    assert "precip" in SYSTEM_PROMPT
    assert "tmax" in SYSTEM_PROMPT
    assert "tmin" in SYSTEM_PROMPT
    assert "evap" in SYSTEM_PROMPT

def test_system_prompt_tiene_limites():
    from scripts.eda_agent.config.agent_setup import SYSTEM_PROMPT
    assert "Prohibido" in SYSTEM_PROMPT

def test_build_agent():
    from scripts.eda_agent.config.agent_setup import build_agent
    with patch("scripts.eda_agent.config.agent_setup.build_llm") as mock_llm:
        mock_llm.return_value = MagicMock()
        agent = build_agent()
        assert agent is not None

def test_build_agent_llama_log():
    from scripts.eda_agent.config.agent_setup import build_agent
    with patch("scripts.eda_agent.config.agent_setup.build_llm") as mock_llm:
        with patch("scripts.eda_agent.config.agent_setup.log_agent_start") as mock_log:
            mock_llm.return_value = MagicMock()
            build_agent(modelo="rapido", temperature=0)
            mock_log.assert_called_once_with(modelo="rapido", n_tools=7)