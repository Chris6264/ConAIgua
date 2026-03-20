import time
import webbrowser
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
from .agent import build_agent

console = Console()

def main():
    agent = build_agent()
    console.print("ConAIgua Fase EDA. Escribe 'salir' para terminar.\n")
    while True:
        user_input = input("Tu pregunta: ").strip()
        if user_input.lower() in ("salir", "exit", "quit"):
            break
        if not user_input:
            continue

        buffer = ""
        for token, metadata in agent.stream(
            {"messages": [("user", user_input)]},
            stream_mode="messages"
        ):
            if token.content:
                buffer += token.content

        if "__HTML__:" in buffer:
            raw = buffer.split("__HTML__:")[1].strip()
            if "\n" in raw:
                raw = raw.split("\n")[0].strip()
            uri = raw.split("|")[0].strip()
            webbrowser.open(uri)
            console.print("\nConAIgua: Reporte generado (abierto en navegador)")

        elif "__MD__:" in buffer:
            content = buffer.split("__MD__:")[1]
            if "\nEl reporte" in content:
                content = content.split("\nEl reporte")[0]
            content = content.strip()
            console.print("\nConAIgua:")
            for char in content:
                print(char, end="", flush=True)
                time.sleep(0.01)

        else:
            console.print("\nConAIgua: ", end="")
            for char in buffer:
                print(char, end="", flush=True)
                time.sleep(0.02)

        print("\n")

if __name__ == "__main__":
    main() 