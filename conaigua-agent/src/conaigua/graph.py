from io import StringIO

from rich.console import Console

from conaigua.core.app_factory import build_app


_silent_output = StringIO()

_silent_console = Console(
    file=_silent_output,
    force_terminal=False,
    width=140,
    record=True,
)

runner, _handler = build_app(_silent_console)

graph = runner.agent