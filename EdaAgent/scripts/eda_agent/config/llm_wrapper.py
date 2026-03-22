import os

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

MODELOS_GROQ = {
    "rapido": "llama-3.1-8b-instant",
    "balanceado": "llama-3.3-70b-versatile",
    "razonamiento": "qwen/qwen3-32b",
}

MODELOS_OPENAI = {
    "rapido": "gpt-4o-mini",
    "balanceado": "gpt-4o",
    "razonamiento": "gpt-4o",
}

MODELOS_ANTHROPIC = {
    "rapido": "claude-haiku-4-5-20251001",
    "balanceado": "claude-sonnet-4-6",
    "razonamiento": "claude-opus-4-6",
}

MODELOS_GOOGLE = {
    "rapido": "gemini-1.5-flash",
    "balanceado": "gemini-1.5-pro",
    "razonamiento": "gemini-1.5-pro",
}


def _get_provider() -> str:
    return os.getenv("LLM_PROVIDER","groq").lower()


def _get_model_name(provider: str, modelo: str) -> str:
    mapping = {
        "groq": MODELOS_GROQ,
        "openai": MODELOS_OPENAI,
        "anthropic": MODELOS_ANTHROPIC,
        "google": MODELOS_GOOGLE,
    }

    if provider not in mapping:
        raise ValueError(
            f"Proveedor '{provider}' no soportado. Usa: groq, openai, anthropic, google"
        )

    return mapping[provider].get(modelo, modelo)

def build_llm(
    modelo: str = "",
    temperature: float = 0,
    max_tokens: int = 1024
):

    if not isinstance(modelo, str):
        raise ValueError("modelo debe ser string")

    provider = _get_provider()
    model_name = _get_model_name(provider, modelo)

    common_kwargs = {
        "temperature": temperature,
    }

    if provider == "groq":
        return ChatGroq(
            model=model_name,
            max_tokens=max_tokens,
            **common_kwargs
        )

    elif provider == "openai":
        return ChatOpenAI(
            model=model_name,
            max_tokens=max_tokens,
            **common_kwargs
        )

    elif provider == "anthropic":
        return ChatAnthropic(
            model=model_name,
            max_tokens=max_tokens,
            **common_kwargs
        )

    elif provider == "google":
        return ChatGoogleGenerativeAI(
            model=model_name,
            max_output_tokens=max_tokens,  
            **common_kwargs
        )

    raise ValueError(f"Proveedor '{provider}' no soportado")