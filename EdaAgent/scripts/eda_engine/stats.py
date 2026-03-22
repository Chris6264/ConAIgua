def compute_stats(df,column):
    series = df[column].dropna()

    if series.empty:
        return None
    
    return {
        "media": float(series.mean()),
        "mediana": float(series.median()),
        "desviacion_estandar": float(series.std()),
        "min": float(series.min()),
        "max": float(series.max()),
        "q1": float(series.quantile(0.25)),
        "q3": float(series.quantile(0.75)),
        "conteo_valido": int(series.count())
    }