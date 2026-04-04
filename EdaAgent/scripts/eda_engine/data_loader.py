import pandas as pd

DATA_PATH = r'data\processed\conAIgua_dataframe.parquet'

def load_dataset():
    return pd.read_parquet(DATA_PATH)

def filter_data(df,estacion_id=None, anio=None):
    if estacion_id:
        df = df[df['estacion_id'] == str(estacion_id)]
    
    if anio:
        df = df[df['anio'] == anio]
    
    return df