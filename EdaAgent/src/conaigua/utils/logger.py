import logging
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"


def get_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        log_path = LOGS_DIR / log_file
        log_path.parent.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def get_pipeline_logger() -> logging.Logger:
    return get_logger("pipeline", "pipeline.log")


def get_agent_logger() -> logging.Logger:
    return get_logger("ConAIgua", "agent.log")


# Logger del agente disponible globalmente
logger = get_agent_logger()


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


__all__ = [
    "logger",
    "get_pipeline_logger",
    "get_agent_logger",
    "log_interaction",
    "log_agent_start",
    "log_error"
]