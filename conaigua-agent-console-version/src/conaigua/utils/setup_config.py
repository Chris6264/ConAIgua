from src.conaigua.utils.config_manager import ConfigManager


LLM_OPTIONS = {
    "1": ("OpenAI", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]),
    "2": ("Groq", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "qwen/qwen3-32b"]),
    "3": ("Gemini", ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-pro"]),
    "4": ("Claude", ["claude-haiku-4-5-20251001", "claude-sonnet-4-6", "claude-3-haiku"])
}


def run_initial_setup():
    print("\nConfiguración inicial\n")

    print("Selecciona proveedor LLM:")
    for key, (name, _) in LLM_OPTIONS.items():
        print(f"{key}. {name}")

    provider_choice = input("Opción: ").strip()
    provider_name, models = LLM_OPTIONS.get(provider_choice, (None, None))

    if not provider_name:
        print("Opción inválida")
        return run_initial_setup()

    print(f"\nModelos disponibles para {provider_name}:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")

    print("4. Escribir modelo manual")

    model_choice = input("Selecciona modelo: ").strip()

    if model_choice == "4":
        model_name = input("Escribe el nombre del modelo: ")
    else:
        try:
            model_name = models[int(model_choice) - 1]
        except:
            print("Opción inválida")
            return run_initial_setup()

    api_key = input("\nIngresa tu API Key: ")

    config = {
        "llm": {
            "provider": provider_name,
            "model": model_name,
            "api_key": api_key
        }
    }

    ConfigManager.save_config(config)

    print("\nConfiguración guardada correctamente\n")

    return config