from typing import Any
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import re

from rich.console import Console

from conaigua.core.app_factory import build_app


_silent_output = StringIO()

_silent_console = Console(
    file=_silent_output,
    force_terminal=False,
    width=140,
    record=True,
)

_runner = None
_handler = None


def init_agent():
    """
    Inicializa el agente una sola vez.

    Este flujo no usa input(), while True ni menús interactivos.
    """
    global _runner, _handler

    if _runner is not None and _handler is not None:
        return _runner, _handler

    _runner, _handler = build_app(_silent_console)

    return _runner, _handler


def normalize_user_input(value: Any) -> str:
    """
    Convierte lo que llega desde la UI a texto plano.

    El chat-ui puede mandar:
    - string
    - lista de bloques
    - diccionario
    - objeto con .content
    """
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, list):
        parts = []

        for item in value:
            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):
                parts.append(
                    str(
                        item.get("text")
                        or item.get("content")
                        or item
                    )
                )

            else:
                parts.append(str(item))

        return "\n".join(parts).strip()

    if isinstance(value, dict):
        return str(
            value.get("text")
            or value.get("content")
            or value
        ).strip()

    if hasattr(value, "content"):
        return normalize_user_input(value.content)

    return str(value).strip()


def extract_answer_from_buffer(buffer: Any) -> str:
    """
    Intenta extraer texto si runner.run() devuelve algo estructurado.
    """
    if buffer is None:
        return ""

    if isinstance(buffer, str):
        return buffer.strip()

    if isinstance(buffer, dict):
        for key in ("answer", "response", "output", "content", "text", "final"):
            if key in buffer:
                return normalize_user_input(buffer[key])

        if "messages" in buffer:
            messages = buffer["messages"]

            if isinstance(messages, list) and messages:
                last_message = messages[-1]

                if hasattr(last_message, "content"):
                    return normalize_user_input(last_message.content)

                if isinstance(last_message, dict):
                    return normalize_user_input(
                        last_message.get("content")
                        or last_message.get("text")
                        or last_message
                    )

    if hasattr(buffer, "content"):
        return normalize_user_input(buffer.content)

    return ""


def clean_agent_output(text: str) -> str:
    """
    Limpia salidas capturadas para que la UI reciba solo la respuesta final.
    """
    if not text:
        return ""

    text = text.strip()

    text = re.sub(
        r"Config cargada:.*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    text = re.sub(
        r"^ConAIgua\s*:\s*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    ).strip()

    return text


def is_useful_answer(text: str) -> bool:
    if not text:
        return False

    normalized = text.strip().lower()

    if normalized in ("conaigua:", "conagua:", "coniaigua:"):
        return False

    if len(normalized) < 3:
        return False

    return True


def ask_conaigua(user_input: Any) -> str:
    """
    Entrada oficial del agente para la UI.

    Recibe un prompt, ejecuta el agente y retorna texto para LangGraph.
    """
    user_input = normalize_user_input(user_input)

    if not user_input:
        return "Por favor escribe una pregunta válida."

    try:
        runner, handler = init_agent()

        stdout_buffer = StringIO()
        stderr_buffer = StringIO()

        result = None
        buffer = None
        rich_output = ""

        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            buffer = runner.run(user_input)

            if handler is not None:
                with _silent_console.capture() as capture:
                    result = handler.handle(user_input, buffer)

                rich_output = capture.get()

        candidates = [
            result if isinstance(result, str) else "",
            rich_output,
            stdout_buffer.getvalue(),
            extract_answer_from_buffer(buffer),
        ]

        for candidate in candidates:
            cleaned = clean_agent_output(candidate)

            if is_useful_answer(cleaned):
                return cleaned

        return "El agente procesó la solicitud, pero no devolvió una respuesta textual."

    except Exception as exc:
        return f"Error al ejecutar el agente ConAIgua: {exc}"