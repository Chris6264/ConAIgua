from langchain_core.tools import tool

from conaigua.eda_engine.data_loader import load_dataset, filter_data
from conaigua.eda_engine.estacion_resolver import EstacionAmbiguaError, EstacionNoEncontradaError


@tool
def filter_tool(estacion_id: str, anio: int = None) -> str:
    """Filtra el dataframe por estación y opcionalmente por año."""
    df = load_dataset()

    try:
        df_filtered = filter_data(df, estacion_id=estacion_id, anio=anio)
    except EstacionAmbiguaError as e:
        opciones = "\n".join(f"- {c}" for c in e.candidatos)
        return f"Encontré varias estaciones que coinciden con '{e.query}'. Pide al usuario que elija una:\n{opciones}"
    except EstacionNoEncontradaError as e:
        return str(e)

    return f'Filtrado: {len(df_filtered)} registros para estación {estacion_id}' + (f', año {anio}' if anio else "")