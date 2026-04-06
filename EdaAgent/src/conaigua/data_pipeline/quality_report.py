import pandas as pd

class QualityReport:

    @staticmethod
    def generate(df: pd.DataFrame) -> pd.DataFrame:
        report = pd.DataFrame({
            "columna": df.columns,
            "nulos": df.isnull().sum().values,
            "no_nulos": df.notnull().sum().values,
            "porcentaje_nulos": (df.isnull().mean() * 100).values
        })

        return report

    @staticmethod
    def save(report: pd.DataFrame, path="data/processed/quality_report.csv"):
        report.to_csv(path, index=False)