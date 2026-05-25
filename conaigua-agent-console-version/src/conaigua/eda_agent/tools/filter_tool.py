from langchain_core.tools import tool
from conaigua.eda_engine.data_loader import load_dataset, filter_data

@tool
def filter_tool(estacion_id: str, anio : int = None) -> str:
    """Filtra el dataframe por estación y opcionalmente por año."""
    df = load_dataset()
    df_filtered = filter_data(df, estacion_id= estacion_id, anio = anio)
    return f'Filtrado: {len(df_filtered)} registros para estación {estacion_id}' + (f', año {anio}' if anio else "")