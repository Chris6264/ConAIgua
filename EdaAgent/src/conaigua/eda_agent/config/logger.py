import logging
import json
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path("logs")
LOG_FILE = LOGS_DIR / "agent.log"


def _get_logger() -> logging.Logger:
    logger = logging.getLogger("ConAIgua")
    LOGS_DIR.mkdir(exist_ok=True)
    has_file_handler = any(
        isinstance(h, logging.FileHandler) for h in logger.handlers
    )
    if not has_file_handler:
        handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


logger = _get_logger()


def _write_log(level: str, entry: dict):
    message = json.dumps(entry, ensure_ascii=False)
    if level == "info":
        logger.info(message)
    elif level == "error":
        logger.error(message)
    for h in logger.handlers:
        if isinstance(h, logging.FileHandler):
            h.flush()


def log_interaction(user_input: str, response: str, tools_used: list = None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "evento": "interaction",
        "user_input": user_input,
        "response": (response or "")[:300],
        "tools_used": tools_used or []
    }
    _write_log("info", entry)


def log_agent_start(modelo: str, n_tools: int):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "evento": "agent_start",
        "modelo": modelo,
        "n_tools": n_tools
    }
    _write_log("info", entry)


def log_error(error: str, user_input: str = None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "evento": "error",
        "user_input": user_input,
        "error": str(error)
    }
    _write_log("error", entry)


__all__ = ["logger", "log_interaction", "log_agent_start", "log_error"]