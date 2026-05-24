import re
import time
import webbrowser
from pathlib import Path
from rich.markdown import Markdown


class ResponseHandler:

    def __init__(self, console):
        self.console = console

    def handle(self, user_input: str, buffer: str):

        if "__HTML__:" in buffer:
            raw = buffer.split("__HTML__:")[1].strip()

            if "\n" in raw:
                raw = raw.split("\n")[0].strip()

            uri = raw.split("|")[0].strip()

            webbrowser.open(uri)

            self.console.print("\nConAIgua: Reporte generado (HTML)")
            return

        if "__MD__:" in buffer:
            raw = buffer.split("__MD__:")[1].strip()
            raw = raw.split(".md")[0].strip() + ".md"

            path = Path(raw)

            if path.exists():
                content = path.read_text(encoding="utf-8")

                self.console.print("\nConAIgua:")

                for line in content.split("\n"):
                    self.console.print(Markdown(line))
                    time.sleep(0.02)
            else:
                self.console.print(f"No se encontró {path}")

            return

        clean = re.sub(r'\{.*\}', '', buffer, flags=re.DOTALL).strip()
        clean = re.sub(r'^[\s,\"\{\}:]+', '', clean).strip()

        self.console.print("\nConAIgua: ", end="")

        for char in clean:
            print(char, end="", flush=True)
            time.sleep(0.01)

        print("\n")