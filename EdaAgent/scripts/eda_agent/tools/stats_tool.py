import json
from langchain_core.tools import tool
from scripts.eda_engine.data_loader import load_dataset, filter_data

@tool
def stats_tool(estacion_id: str, variable: str = "precip", anio: int = None) -> str:
    """
    Calcula estadísticas básicas de una variable para una estación.
    Retorna datos internos — NO mostrar el JSON al usuario, solo interpretar.
    Variables disponibles: precip, evap, tmax, tmin.
    """
    df = load_dataset()
    df_f = filter_data(df, estacion_id=estacion_id, anio=anio)
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