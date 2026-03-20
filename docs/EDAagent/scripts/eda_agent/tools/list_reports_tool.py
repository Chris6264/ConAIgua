from pathlib import Path
from langchain_core.tools import tool

@tool
def list_reports_tool(estacion_id: str = None) -> str:
    """Lista los reportes EDA ya generados. Filtra por estación si se proporciona."""
    reports_dir = Path("reports/eda")
    if not reports_dir.exists():
        return "No existe el directorio de reportes."
    files = list(reports_dir.glob("*.html")) + list(reports_dir.glob("*.md"))
    if estacion_id:
        files = [f for f in files if estacion_id in f.name]
    if not files:
        return "No se encontraron reportes."
    return "\n".join(str(f) for f in sorted(files))

@tool
def read_report_tool(estacion_id: str, formato: str = "markdown") -> str:
    """Lee y retorna el contenido de un reporte ya generado."""
    from pathlib import Path
    if formato == "markdown":
        path = Path(f"reports/eda/eda_station_{estacion_id}.md")
        if path.exists():
            return path.read_text(encoding="utf-8")
        return f"No existe reporte markdown para estación {estacion_id}."
    
@tool
def open_html_report_tool(estacion_id: str) -> str:
    """Abre el reporte HTML de una estación en el navegador."""
    from pathlib import Path
    path = Path(f"reports/eda/eda_station_{estacion_id}.html")
    if path.exists():
        print(path.resolve().as_uri())
        return f"Reporte HTML abierto en el navegador para estación {estacion_id}."
    return f"No existe reporte HTML para estación {estacion_id}. ¿Deseas generarlo?"