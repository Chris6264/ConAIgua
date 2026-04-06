def test_prompt_contiene_contexto():
    from conaigua.eda_agent.config.agent_setup import SYSTEM_PROMPT

    assert "ConAIgua" in SYSTEM_PROMPT
    assert "CONAGUA" in SYSTEM_PROMPT


def test_prompt_tiene_capacidades():
    from conaigua.eda_agent.config.agent_setup import SYSTEM_PROMPT

    assert "Capacidades" in SYSTEM_PROMPT


def test_prompt_variables():
    from conaigua.eda_agent.config.agent_setup import SYSTEM_PROMPT

    assert "precip" in SYSTEM_PROMPT
    assert "tmax" in SYSTEM_PROMPT
    assert "tmin" in SYSTEM_PROMPT
    assert "evap" in SYSTEM_PROMPT


def test_prompt_limites():
    from conaigua.eda_agent.config.agent_setup import SYSTEM_PROMPT

    assert "Prohibido" in SYSTEM_PROMPT