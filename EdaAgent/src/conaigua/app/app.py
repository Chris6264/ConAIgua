import argparse
from rich.console import Console

from conaigua.core.config_service import handle_config
from conaigua.core.app_factory import build_app

console = Console()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--reset-config", action="store_true")
    return parser.parse_args()


def run_app():
    args = parse_args()

    config = handle_config(args, console)

    runner, handler = build_app(console)

    console.print("\n[bold]ConAIgua Fase EDA[/bold]. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tu pregunta: ").strip()

        if user_input.lower() in ("salir", "exit", "quit"):
            break

        if not user_input:
            continue

        try:
            buffer = runner.run(user_input)
            handler.handle(user_input, buffer)

        except Exception as e:
            console.print(f"[red]{str(e)}[/red]")