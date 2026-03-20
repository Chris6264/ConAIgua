import json
from langchain_core.tools import tool
from scripts.eda_engine.data_loader import load_dataset, filter_data
from scripts.eda_engine.eda_pipeline import run_eda

@tool
def eda_tool(estacion_id : str, variable: str, anio : int = None) -> str:
    """
    Ejecuta análisis EDA sobre una estación.
    Variables disponibles: precip, evap, tmax, tmin.
    Retorna estad   sticas, outliers y estacionalidad.
    """
    df = load_dataset()
    df_filtered = filter_data(df, estacion_id = estacion_id, anio = anio)
    
    if df_filtered.empty:
        return f"No se encontraron datos para estación {estacion_id}" + (f" año {anio}" if anio else "")
    
    result = run_eda(df_filtered,variable)
    return json.dumps(result, ensure_ascii = False, indent = 2)