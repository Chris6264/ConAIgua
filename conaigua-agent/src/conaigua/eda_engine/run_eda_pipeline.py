from conaigua.eda_engine.stats import compute_stats
from conaigua.eda_engine.outliers import detect_outliers_iqr
from conaigua.eda_engine.seasonality import monthly_pattern

def run_eda(df,column):
    stats = compute_stats(df,column)
    outliers = detect_outliers_iqr(df,column)
    seasonality = monthly_pattern(df,column)

    return {
        "variable" : column,
        "estadisticos": stats,
        "outliers": outliers,
        "estacionalidad": seasonality   
    }