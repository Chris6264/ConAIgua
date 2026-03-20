from pathlib import Path
from langchain_core.tools import tool
from scripts.eda_reports_generator.html_generator import generate_station_html_report
from scripts.eda_reports_generator.markdown_generator import generate_station_markdown_report

@tool
def report_tool(estacion_id: str, formato: str = "markdown") -> str:
    """
    Verifica si existe un reporte EDA para una estación.
    Si existe lo usa, si no lo genera.
    formato: 'html' o 'markdown'. Por defecto markdown.
    """
    html_path = Path(f"reports/eda/html/eda_station_{estacion_id}.html")
    md_path = Path(f"reports/eda/markdown/eda_station_{estacion_id}.md")

    if formato == "html":
        if not html_path.exists():
            generate_station_html_report(estacion_id)
        return f"__HTML__:{html_path.resolve().as_uri()}|{html_path}"

    elif formato == "markdown":
        if not md_path.exists():
            generate_station_markdown_report(estacion_id)
        return f"__MD__:{md_path.read_text(encoding='utf-8')}"

    return "Formato no reconocido."