from conaigua.utils.config_manager import ConfigManager


def handle_config(args, console):

    if args.reset_config:
        ConfigManager.reset_config()
        console.print("[red]Configuración eliminada[/red]")
        ConfigManager.create_config()

    elif args.setup:
        ConfigManager.create_config()

    if not ConfigManager.config_exists():
        ConfigManager.create_config()

    config = ConfigManager.load_config()
    llm = config["llm"]

    console.print(
        f"[green]Config cargada:[/green] {llm['provider']} - {llm['model']}"
    )

    return config