import pandas as pd
from pathlib import Path
from conaigua.eda_engine.estacion_resolver import resolve_estacion_id_or_raise


DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "data" / "processed" / "conAIgua_dataframe.parquet"

def load_dataset():
    return pd.read_parquet(DATA_PATH)

def filter_data(df: pd.DataFrame, estacion_id: str = None, anio: int = None) -> pd.DataFrame:
    if estacion_id is not None:
        resolved_id = resolve_estacion_id_or_raise(df, str(estacion_id).strip())
        df = df[df["estacion_id"].astype(str) == resolved_id]

    if anio is not None:
        df = df[df["anio"] == anio]

    return df