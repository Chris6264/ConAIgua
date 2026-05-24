from pathlib import Path
from langchain_core.tools import tool
from conaigua.eda_reports_generator.html_generator import generate_station_html_report
from conaigua.eda_reports_generator.markdown_generator import generate_station_markdown_report
from conaigua.eda_engine.data_loader import load_dataset

@tool
def report_tool(estacion_id: str, formato: str = "markdown") -> str:
    """
    Genera o recupera el reporte EDA de una estación.
    Cuando esta tool retorna un resultado exitoso, NO agregues comentarios
    ni texto adicional. Solo confirma que el reporte fue procesado.
    formato: 'html' o 'markdown'. Por defecto markdown.
    """
    df = load_dataset()
    if estacion_id not in df["estacion_id"].values:
        return f"No tengo datos para la estación {estacion_id}."

    html_path = Path(f"reports/eda/html/eda_station_{estacion_id}.html")
    md_path = Path(f"reports/eda/markdown/eda_station_{estacion_id}.md")

    if formato == "html":
        if not html_path.exists():
            generate_station_html_report(estacion_id)
        return f"__HTML__:{html_path.resolve().as_uri()}|{html_path}"

    elif formato == "markdown":
        if not md_path.exists():
            generate_station_markdown_report(estacion_id)
        return f"__MD__:{md_path}"

    return "Formato no reconocido."