from pathlib import Path
import yaml


class ConfigManager:

    CONFIG_PATH = Path("config/config.yaml")

    PROVIDERS = ["openai", "groq", "anthropic", "google"]

    MODELOS = {
    "openai": ["gpt-4o-mini", "gpt-4o", "o3-mini"],
    "groq": ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "qwen/qwen3-32b"],
    "anthropic": ["claude-haiku-4-5", "claude-sonnet-4-5", "claude-opus-4-5"],
    "google": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
    }

    @classmethod
    def config_exists(cls) -> bool:
        return cls.CONFIG_PATH.exists()

    @classmethod
    def load_config(cls) -> dict:
        if not cls.config_exists():
            raise FileNotFoundError("No existe config.yaml")

        with open(cls.CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @classmethod
    def _select_option(cls, title, options):
        print(f"\n{title}")
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        print("0. Manual")

        while True:
            choice = input("Selecciona opción: ").strip()

            if choice == "0":
                return input("Escribe valor manual: ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice) - 1]

            print("Opción inválida, intenta de nuevo.")

    @classmethod
    def create_config(cls):
        print("\nConfiguración inicial\n")

        provider = cls._select_option("Selecciona proveedor:", cls.PROVIDERS).lower()

        modelos = cls.MODELOS.get(provider, [])
        model = cls._select_option("Selecciona modelo:", modelos)

        api_key = input("\nAPI Key: ").strip()

        config = {
            "llm": {
                "provider": provider,
                "model": model,
                "api_key": api_key,
                "temperature": 0,
                "max_tokens": 1024,
            }
        }

        cls.CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(cls.CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.dump(config, f, sort_keys=False)

        print("\nConfiguración guardada")

    @classmethod
    def reset_config(cls):
        if cls.CONFIG_PATH.exists():
            cls.CONFIG_PATH.unlink()