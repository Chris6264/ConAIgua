from pathlib import Path

from langchain_core.tools import tool

from conaigua.eda_reports_generator.html_generator import generate_station_html_report
from conaigua.eda_reports_generator.markdown_generator import generate_station_markdown_report
from conaigua.eda_engine.data_loader import load_dataset


REPORTS_DIR = Path("reports")
REPORTS_BASE_URL = "http://localhost:8088"


def build_report_url(report_path: Path) -> str:
    reports_root = REPORTS_DIR.resolve()
    report_path = report_path.resolve()

    relative_path = report_path.relative_to(reports_root)

    return f"{REPORTS_BASE_URL}/{relative_path.as_posix()}"


@tool
def report_tool(estacion_id: str, formato: str = "markdown") -> str:
    """
    Genera o recupera el reporte EDA de una estación.

    IMPORTANTE PARA EL AGENTE:
    Después de usar esta herramienta, responde al usuario repitiendo exactamente
    el enlace generado por la herramienta en formato Markdown.
    No respondas solo 'HTML' o 'Markdown'.
    """
    df = load_dataset()

    estacion_id = str(estacion_id).strip()
    formato = str(formato).strip().lower()

    if estacion_id not in df["estacion_id"].astype(str).values:
        return f"No tengo datos para la estación {estacion_id}."

    html_path = Path(f"reports/eda/html/eda_station_{estacion_id}.html")
    md_path = Path(f"reports/eda/markdown/eda_station_{estacion_id}.md")

    html_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    if formato == "html":
        if not html_path.exists():
            generate_station_html_report(estacion_id)

        report_url = build_report_url(html_path)

        return (
            "Reporte HTML generado correctamente.\n\n"
            f"[Abrir reporte HTML]({report_url})\n\n"
            f"URL directa: {report_url}"
        )

    if formato == "markdown":
        if not md_path.exists():
            generate_station_markdown_report(estacion_id)

        return (
            "Reporte Markdown generado correctamente.\n\n"
            f"Ruta local: `{md_path}`"
        )

    return "Formato no reconocido. Usa 'html' o 'markdown'."