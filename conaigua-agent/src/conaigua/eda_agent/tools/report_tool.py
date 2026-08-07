import unicodedata
from pathlib import Path

import pandas as pd
from langchain_core.tools import tool

from conaigua.eda_reports_generator.html_generator import generate_station_html_report
from conaigua.eda_reports_generator.markdown_generator import generate_station_markdown_report
from conaigua.eda_engine.data_loader import load_dataset


REPORTS_DIR = Path("reports")
REPORTS_BASE_URL = "http://localhost:8088"
NOMBRE_COL = "nombre_estacion"


def build_report_url(report_path: Path) -> str:
    reports_root = REPORTS_DIR.resolve()
    report_path = report_path.resolve()
    relative_path = report_path.relative_to(reports_root)
    return f"{REPORTS_BASE_URL}/{relative_path.as_posix()}"


def _normalize(text: str) -> str:
    text = str(text).strip().upper()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.split())


def resolve_estacion_id(df: pd.DataFrame, query: str) -> tuple[str | None, list[str]]:
    query_norm = _normalize(query)

    ids = df["estacion_id"].astype(str)
    if query.strip() in ids.values:
        return query.strip(), []

    if NOMBRE_COL not in df.columns:
        return None, []

    nombres_norm = df[NOMBRE_COL].astype(str).map(_normalize)

    exact_matches = df.loc[nombres_norm == query_norm, "estacion_id"].astype(str).unique()
    if len(exact_matches) == 1:
        return exact_matches[0], []
    if len(exact_matches) > 1:
        return None, list(exact_matches)

    partial_mask = nombres_norm.str.contains(query_norm, na=False)
    partial_matches = df.loc[partial_mask, ["estacion_id", NOMBRE_COL]].drop_duplicates()

    if len(partial_matches) == 1:
        return str(partial_matches.iloc[0]["estacion_id"]), []
    if len(partial_matches) > 1:
        candidatos = [
            f"{row['estacion_id']} ({row[NOMBRE_COL]})"
            for _, row in partial_matches.iterrows()
        ]
        return None, candidatos

    return None, []


@tool
def report_tool(estacion_id: str, formato: str = "html") -> str:
    """
    Genera o recupera el reporte EDA de una estación.

    El parámetro estacion_id acepta tanto la clave numérica de la estación
    (ej. "25161") como su nombre (ej. "El Dorado"), y también nombres
    parciales (ej. "dorado").

    Formatos disponibles:
    - html
    - markdown

    Si el usuario no especifica formato, usa html.
    Si el usuario pide markdown, lee el archivo .md y devuelve su contenido
    para que el agente lo muestre en la respuesta final.
    """
    df = load_dataset()

    estacion_id = str(estacion_id).strip()
    formato = str(formato or "html").strip().lower()

    resolved_id, candidatos = resolve_estacion_id(df, estacion_id)

    if resolved_id is None and candidatos:
        opciones = "\n".join(f"- {c}" for c in candidatos)
        return (
            "RESPUESTA_FINAL_PARA_USUARIO:\n"
            f"Encontré varias estaciones que coinciden con '{estacion_id}'. "
            f"¿Cuál te refieres?\n\n{opciones}"
        )

    if resolved_id is None:
        return (
            "RESPUESTA_FINAL_PARA_USUARIO:\n"
            f"No tengo datos para la estación {estacion_id}."
        )

    estacion_id = resolved_id

    html_path = Path(f"reports/eda/html/eda_station_{estacion_id}.html")
    md_path = Path(f"reports/eda/markdown/eda_station_{estacion_id}.md")

    html_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    if formato == "html":
        if not html_path.exists():
            generate_station_html_report(estacion_id)

        report_url = build_report_url(html_path)

        return (
            "RESPUESTA_FINAL_PARA_USUARIO:\n"
            "Listo, reporte generado con éxito.\n\n"
            f"[Abrir reporte HTML]({report_url})"
        )

    if formato in ("markdown", "md"):
        if not md_path.exists():
            generate_station_markdown_report(estacion_id)

        markdown_content = md_path.read_text(encoding="utf-8")

        return (
            "RESPUESTA_FINAL_PARA_USUARIO:\n"
            "Listo, reporte Markdown generado con éxito.\n\n"
            f"{markdown_content}"
        )

    return (
        "RESPUESTA_FINAL_PARA_USUARIO:\n"
        "Formato no reconocido. Usa 'html' o 'markdown'."
    )