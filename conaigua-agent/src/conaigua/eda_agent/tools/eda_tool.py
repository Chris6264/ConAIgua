import json

from langchain_core.tools import tool

from conaigua.eda_engine.data_loader import load_dataset, filter_data
from conaigua.eda_engine.run_eda_pipeline import run_eda
from conaigua.eda_engine.estacion_resolver import EstacionAmbiguaError, EstacionNoEncontradaError


@tool
def eda_tool(estacion_id: str, variable: str, anio: int = None) -> str:
    """
    Ejecuta análisis EDA sobre una estación.
    El parámetro estacion_id acepta clave numérica o nombre (exacto o parcial).
    Variables disponibles: precip, evap, tmax, tmin.
    Retorna estadísticas, outliers y estacionalidad.
    """
    df = load_dataset()

    try:
        df_filtered = filter_data(df, estacion_id=estacion_id, anio=anio)
    except EstacionAmbiguaError as e:
        opciones = "\n".join(f"- {c}" for c in e.candidatos)
        return f"Encontré varias estaciones que coinciden con '{e.query}'. Pide al usuario que elija una:\n{opciones}"
    except EstacionNoEncontradaError as e:
        return str(e)

    if df_filtered.empty:
        return f"No se encontraron datos para estación {estacion_id}" + (f" año {anio}" if anio else "")

    result = run_eda(df_filtered, variable)
    return json.dumps(result, ensure_ascii=False, indent=2)