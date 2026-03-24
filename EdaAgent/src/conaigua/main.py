import re
import sys
import time
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

from scripts.eda_agent.config.agent_setup import build_agent
from scripts.eda_agent.config.logger import log_interaction, log_error

console = Console()
CONFIG = {"configurable": {"thread_id": "conaigua_session"}}

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
        try:
            for token, metadata in agent.stream(
                {"messages": [("user", user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if token.content:
                    buffer += token.content
        except Exception as e:
            log_error(str(e), user_input)
            console.print(f"\n[red]ERROR: {e}[/red]\n")  
            continue

        if "__HTML__:" in buffer:
            raw = buffer.split("__HTML__:")[1].strip()
            if "\n" in raw:
                raw = raw.split("\n")[0].strip()
            uri = raw.split("|")[0].strip()
            webbrowser.open(uri)
            console.print("\nConAIgua: Reporte generado (abierto en navegador)")
            log_interaction(user_input, "Reporte HTML generado", ["report_tool"])

        elif "__MD__:" in buffer:
            raw = buffer.split("__MD__:")[1].strip()
            raw = raw.split(".md")[0].strip() + ".md"
            raw = raw.split("\n")[0].strip()
            md_path = Path(raw)
            if md_path.exists():
                content = md_path.read_text(encoding="utf-8")
                console.print("\nConAIgua:")
                for line in content.split("\n"):
                    console.print(Markdown(line))
                    time.sleep(0.05)
                log_interaction(user_input, "Reporte MD mostrado", ["report_tool"])
            else:
                console.print(f"\nConAIgua: No se encontró el reporte en {md_path}")

        else:
            console.print("\nConAIgua: ", end="")
            clean = re.sub(r'\{.*\}', '', buffer, flags=re.DOTALL).strip()
            clean = re.sub(r'^[\s,\"\{\}:]+', '', clean).strip()
            for char in clean:
                print(char, end="", flush=True)
                time.sleep(0.02)
            log_interaction(user_input, clean)

        print("\n")

if __name__ == "__main__":
    main()