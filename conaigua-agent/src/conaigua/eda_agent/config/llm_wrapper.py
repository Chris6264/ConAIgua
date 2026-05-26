from conaigua.utils.config_manager import ConfigManager

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI


def build_llm():

    config = ConfigManager.load_config()
    llm_config = config["llm"]

    provider = llm_config["provider"].lower()
    model = llm_config["model"]
    api_key_env = llm_config["api_key_env"]
    temperature = llm_config.get("temperature", 0)
    max_tokens = llm_config.get("max_tokens", 1024)

    if provider == "groq":
        return ChatGroq(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key_env
        )

    elif provider == "openai":
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key_env
        )

    elif provider == "anthropic":
        return ChatAnthropic(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key_env
        )

    elif provider == "google":
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            max_output_tokens=max_tokens,
            google_api_key=api_key_env
        )

    raise ValueError(f"Proveedor no soportado: {provider}")