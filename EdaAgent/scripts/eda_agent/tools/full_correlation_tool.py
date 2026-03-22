import json
from langchain_core.tools import tool
from scripts.eda_engine.data_loader import load_dataset, filter_data
from scripts.eda_engine.correlation import compute_correlations

@tool
def full_correlation_tool(
    estacion_id: str,
    var1: str,
    var2: str,
    anio: int = None
) -> str:
    """
    Calcula correlación Pearson y Spearman entre dos variables para una estación.
    Incluye p-value e interpretación de significancia estadística.
    Variables disponibles: precip, evap, tmax, tmin, mes, anio.
    NO mostrar JSON al usuario, solo interpretar en lenguaje natural.
    """
    df = load_dataset()
    df_f = filter_data(df, estacion_id=estacion_id, anio=anio)
    if df_f.empty:
        return f"No hay datos para estación {estacion_id}."

    for var in [var1, var2]:
        if var not in df_f.columns:
            return f"Variable '{var}' no encontrada. Disponibles: {list(df_f.columns)}"

    result = compute_correlations(df_f, var1, var2)
    return json.dumps(result, ensure_ascii=False)