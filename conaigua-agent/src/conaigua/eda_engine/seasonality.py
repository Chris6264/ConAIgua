def monthly_pattern(df,column):
    df = df.dropna(subset = [column])

    if df.empty:
        return None
    
    monthly = df.groupby("mes")[column].mean()

    return {
        "serie_mensual": monthly.to_dict(),
        "mes_maximo": int(monthly.idxmax()),
        "mes_minimo": int(monthly.idxmin())
    }