import json

from langchain_core.tools import tool

from conaigua.eda_engine.data_loader import load_dataset, filter_data
from conaigua.eda_engine.regression import linear_regression, multiple_regression
from conaigua.eda_engine.estacion_resolver import EstacionAmbiguaError, EstacionNoEncontradaError


@tool
def regression_tool(
    estacion_id: str,
    variable_y: str,
    variables_x: str,
    anio: int = None
) -> str:
    """
    Calcula regresión lineal simple o múltiple para una estación.
    El parámetro estacion_id acepta clave numérica o nombre (exacto o parcial).
    variable_y: variable dependiente (precip, evap, tmax, tmin).
    variables_x: variables independientes separadas por coma.
    Ejemplos: 'mes' para simple, 'mes,anio' para múltiple.
    Incluye coeficientes, R2, RMSE, intervalos de confianza 95% y diagnóstico.
    NO mostrar JSON al usuario, solo interpretar en lenguaje natural.
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
        return f"No hay datos para estación {estacion_id}."

    x_cols = [c.strip() for c in variables_x.split(",")]

    for col in x_cols + [variable_y]:
        if col not in df_f.columns:
            return f"Variable '{col}' no encontrada. Disponibles: {list(df_f.columns)}"

    if len(x_cols) == 1:
        result = linear_regression(df_f, x_cols[0], variable_y)
    else:
        result = multiple_regression(df_f, x_cols, variable_y)

    return json.dumps(result, ensure_ascii=False)