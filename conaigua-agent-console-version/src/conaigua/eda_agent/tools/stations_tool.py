import json
from langchain_core.tools import tool
from conaigua.eda_engine.data_loader import load_dataset

@tool
def stations_tool() -> str:
    """
    Lista todas las estaciones meteorológicas disponibles en el dataset.
    Retorna ID, nombre y total de registros por estación.
    NO mostrar JSON al usuario, interpretar en lenguaje natural.
    """
    df = load_dataset()
    resumen = (
        df.groupby(["estacion_id", "nombre_estacion"])
        .agg(total_registros=("precip", "count"))
        .reset_index()
        .sort_values("estacion_id")
    )
    estaciones = resumen.to_dict(orient="records")
    return json.dumps({
        "total_estaciones": len(estaciones),
        "estaciones": estaciones
    }, ensure_ascii=False)