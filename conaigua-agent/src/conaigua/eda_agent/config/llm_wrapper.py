import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI


PROJECT_ROOT = Path(__file__).resolve().parents[4]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"
ENV_PATH = PROJECT_ROOT / ".env"


def load_config() -> dict:
    """
    Carga la configuración principal del agente desde config/config.yaml.
    También carga variables de entorno desde .env.
    """
    load_dotenv(ENV_PATH)

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de configuración: {CONFIG_PATH}. "
            "Crea config/config.yaml a partir de config/config.example.yaml."
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError("El archivo config/config.yaml está vacío.")

    return config


def get_api_key(api_key_env: str) -> str:
    """
    Recibe el nombre de la variable de entorno, por ejemplo GROQ_API_KEY,
    y devuelve su valor real desde .env.
    """
    api_key = os.getenv(api_key_env)

    if not api_key:
        raise ValueError(
            f"No se encontró la variable de entorno '{api_key_env}'. "
            "Verifica tu archivo .env."
        )

    return api_key


def build_llm():
    config = load_config()
    llm_config = config["llm"]

    provider = llm_config["provider"].lower()
    model = llm_config["model"]
    api_key_env = llm_config["api_key_env"]
    temperature = llm_config.get("temperature", 0)
    max_tokens = llm_config.get("max_tokens", 1024)

    api_key = get_api_key(api_key_env)

    if provider == "groq":
        return ChatGroq(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
        )

    if provider == "openai":
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
        )

    if provider == "anthropic":
        return ChatAnthropic(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
        )

    if provider == "google":
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            max_output_tokens=max_tokens,
            google_api_key=api_key,
        )

    raise ValueError(f"Proveedor no soportado: {provider}")