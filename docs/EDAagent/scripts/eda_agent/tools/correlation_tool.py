import json
from langchain_core.tools import tool
from scripts.eda_engine.data_loader import load_dataset,filter_data

@tool
def correlation_tool(estacion_id : str, var1 : str, var2 : str, anio : int = None) -> str:
    """
    Calcula correlación entre dos variables para una estación.
    Variables disponibles: precip, evap, tmax, tmin.
    """
    df = load_dataset()
    df_filtered = filter_data(df, estacion_id = estacion_id, anio = anio)
    
    if df_filtered.empty:
        return "No se encuentra datos."
    
    if var1 not in df_filtered.columns or var2 not in df_filtered.columns:
        return f"Variables disponibles: {list(df_filtered.columns)}"
    
    corr = df_filtered[[var1,var2]].corr().iloc[0 , 1]
    return json.dumps({
        "estacion_id" : estacion_id,
        "anio": anio,
        "var1" : var1,
        "var2": var2,
        "correlacion_pearson" : round(corr, 4)
    }, ensure_ascii= False)