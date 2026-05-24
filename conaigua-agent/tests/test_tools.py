def test_tools_tienen_nombre():
    from conaigua.eda_agent.config.agent_setup import TOOLS

    for tool in TOOLS:
        assert tool.name, f"Tool sin nombre"


def test_tools_tienen_docstring():
    from conaigua.eda_agent.config.agent_setup import TOOLS

    for tool in TOOLS:
        assert tool.description, f"Tool '{tool.name}' sin descripción"


def test_tools_nombres_unicos():
    from conaigua.eda_agent.config.agent_setup import TOOLS

    nombres = [tool.name for tool in TOOLS]
    assert len(nombres) == len(set(nombres))