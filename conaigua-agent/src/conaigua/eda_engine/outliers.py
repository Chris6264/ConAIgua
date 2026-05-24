def detect_outliers_iqr(df, column):
    series = df[column].dropna()

    if series.empty:
        return {"cantidad" : 0, "indices" : []}
    
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = series[(series < lower) | (series > upper)]

    return {
        "cantidad": int(len(outliers)),
        "valores": outliers.tolist()
    }