import json

import numpy as np
from langchain_core.tools import tool

from conaigua.eda_engine.data_loader import load_dataset, filter_data
from conaigua.eda_engine.estacion_resolver import EstacionAmbiguaError, EstacionNoEncontradaError


@tool
def trend_tool(estacion_id: str, variable: str, anio_inicio: int = None, anio_fin: int = None) -> str:
    """
    Calcula la tendencia anual de una variable para una estación en un rango de años.
    El parámetro estacion_id acepta clave numérica o nombre (exacto o parcial).
    Usa regresión lineal simple. Variables: precip, evap, tmax, tmin.
    """
    df = load_dataset()

    try:
        df_f = filter_data(df, estacion_id=estacion_id)
    except EstacionAmbiguaError as e:
        opciones = "\n".join(f"- {c}" for c in e.candidatos)
        return f"Encontré varias estaciones que coinciden con '{e.query}'. Pide al usuario que elija una:\n{opciones}"
    except EstacionNoEncontradaError as e:
        return str(e)

    if anio_inicio:
        df_f = df_f[df_f["anio"] >= anio_inicio]
    if anio_fin:
        df_f = df_f[df_f["anio"] <= anio_fin]
    if df_f.empty:
        return "No se encontraron datos para el rango especificado."

    anual = df_f.groupby("anio")[variable].sum().reset_index()
    x = anual["anio"].values
    y = anual[variable].values
    coef = np.polyfit(x, y, 1)
    return json.dumps({
        "estacion_id": estacion_id,
        "variable": variable,
        "anio_inicio": int(x.min()),
        "anio_fin": int(x.max()),
        "pendiente_anual": round(coef[0], 4),
        "tendencia": "creciente" if coef[0] > 0 else "decreciente",
        "datos_anuales": anual.to_dict(orient="records")
    }, ensure_ascii=False)