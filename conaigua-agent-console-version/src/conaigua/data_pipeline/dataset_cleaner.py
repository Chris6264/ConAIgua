import pandas as pd

class DataFrameCleaner:

    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        cols_to_clean = [col for col in df.columns if col != "cve_omm"]
        df[cols_to_clean] = df[cols_to_clean].replace("Nulo", pd.NA)

        if "fecha" in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], format="%d/%m/%Y", errors="coerce")
            df['anio'] = df['fecha'].dt.year
            df['mes'] = df['fecha'].dt.month
            df['dia'] = df['fecha'].dt.day

        for col in ['latitud', 'longitud']:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(r'[^\d\.-]', '', regex=True),
                    errors='coerce'
                )

        if "altitud_msnm" in df.columns:
            df['altitud_msnm'] = pd.to_numeric(
                df['altitud_msnm'].astype(str).str.replace(r'[^\d\.]', '', regex=True),
                errors='coerce'
            )

        for col in ['precip', 'evap', 'tmax', 'tmin']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        if "precip" in df.columns:
            df = df[(df["precip"].isna()) | (df["precip"] >= 0)]

        if "tmax" in df.columns:
            df = df[(df["tmax"].between(-50, 60)) | (df["tmax"].isna())]

        if "tmin" in df.columns:
            df = df[(df["tmin"].between(-50, 60)) | (df["tmin"].isna())]

        df = df.drop_duplicates()

        cols = [c for c in ['precip', 'evap', 'tmax', 'tmin'] if c in df.columns]
        if cols:
            df[cols] = df[cols].fillna(0)

        return df