import json

from langchain_core.tools import tool

from conaigua.eda_engine.data_loader import load_dataset, filter_data
from conaigua.eda_engine.estacion_resolver import EstacionAmbiguaError, EstacionNoEncontradaError


@tool
def stats_tool(estacion_id: str, variable: str = "precip", anio: int = None) -> str:
    """
    Calcula estadísticas básicas de una variable para una estación.
    El parámetro estacion_id acepta clave numérica o nombre (exacto o parcial).
    Retorna datos internos — NO mostrar el JSON al usuario, solo interpretar.
    Variables disponibles: precip, evap, tmax, tmin.
    """
    df = load_dataset()

    try:
        df_f = filter_data(df, estacion_id=estacion_id, anio=anio)
    except EstacionAmbiguaError as e:
        opciones = "\n".join(f"- {c}" for c in e.candidatos)
        return f"Encontré varias estaciones que coinciden con '{e.query}'. Pide al usuario que elija una:\n{opciones}"
    except EstacionNoEncontradaError as e:
        return str(e)

    if df_f.empty:
        return f"No se encontraron datos para estación {estacion_id}."
    if variable not in df_f.columns:
        return f"Variable '{variable}' no encontrada. Disponibles: {list(df_f.columns)}"

    serie = df_f[variable].dropna()
    return json.dumps({
        "estacion_id": estacion_id,
        "variable": variable,
        "anio": anio,
        "promedio": round(float(serie.mean()), 4),
        "mediana": round(float(serie.median()), 4),
        "minimo": round(float(serie.min()), 4),
        "maximo": round(float(serie.max()), 4),
        "desviacion_std": round(float(serie.std()), 4),
        "total_registros": int(serie.count())
    }, ensure_ascii=False)