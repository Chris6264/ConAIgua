import pandas as pd

class DataFrameCleaner:

    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

        df['evap'] = df['evap'].replace("Nulo", pd.NA)  # ← primero esto

        df['fecha'] = pd.to_datetime(df['fecha'], format="%d/%m/%Y", errors="coerce")
        df['anio']  = df['fecha'].dt.year
        df['mes']   = df['fecha'].dt.month
        df['dia']   = df['fecha'].dt.day

        for col in ['latitud', 'longitud']:
            df[col] = pd.to_numeric(
                df[col].str.replace(r'[°º\?ï¿½]+', '', regex=True).str.strip(),
                errors='coerce'
            )

        df['altitud_msnm'] = pd.to_numeric(
            df['altitud_msnm'].astype(str).str.replace(r'[^\d\.]', '', regex=True),
            errors='coerce'
        )

        for col in ['precip', 'evap', 'tmax', 'tmin']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['evap'] = df['evap'].fillna(0)  

        return df