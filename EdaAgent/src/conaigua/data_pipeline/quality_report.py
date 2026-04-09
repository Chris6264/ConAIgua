import pandas as pd
import json
from pathlib import Path
from datetime import datetime


class QualityReport:

    @staticmethod
    def generate(df: pd.DataFrame) -> pd.DataFrame:

        # Completitud
        nulos = df.isnull().sum()
        no_nulos = df.notnull().sum()
        porcentaje_nulos = (df.isnull().mean() * 100).round(2)
        completitud = (100 - porcentaje_nulos).round(2)

        # Consistencia - valores duplicados por columna
        duplicados = pd.Series(
            [df.duplicated(subset=[col]).sum() for col in df.columns],
            index=df.columns
        )

        # Precisión - valores fuera de rango para variables numéricas
        rangos = {
            "precip": (0, 1000),
            "evap": (0, 500),
            "tmax": (-10, 60),
            "tmin": (-20, 50),
        }

        fuera_de_rango = []
        for col in df.columns:
            if col in rangos:
                min_val, max_val = rangos[col]
                fuera = ((df[col] < min_val) | (df[col] > max_val)).sum()
                fuera_de_rango.append(fuera)
            else:
                fuera_de_rango.append(None)

        report = pd.DataFrame({
            "columna": df.columns,
            "tipo": df.dtypes.values,
            "nulos": nulos.values,
            "no_nulos": no_nulos.values,
            "porcentaje_nulos": porcentaje_nulos.values,
            "completitud_%": completitud.values,
            "duplicados": duplicados.values,
            "fuera_de_rango": fuera_de_rango,
        })

        return report

    @staticmethod
    def save(report: pd.DataFrame, path="data/processed/quality_report.csv"):
        report.to_csv(path, index=False)

    @staticmethod
    def generate_html(report: pd.DataFrame, df: pd.DataFrame, path: Path):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_registros = len(df)
        completitud_global = round(100 - df.isnull().mean().mean() * 100, 2)
        duplicados_totales = df.duplicated().sum()

        filas = ""
        for _, row in report.iterrows():
            fuera = row["fuera_de_rango"]
            fuera_str = str(int(fuera)) if pd.notna(fuera) else "N/A"
            completitud = row["completitud_%"]
            color = "#2ecc71" if completitud >= 90 else "#e67e22" if completitud >= 70 else "#e74c3c"

            filas += f"""
            <tr>
                <td>{row['columna']}</td>
                <td>{row['tipo']}</td>
                <td>{int(row['nulos'])}</td>
                <td>{int(row['no_nulos'])}</td>
                <td>{row['porcentaje_nulos']}%</td>
                <td style="color:{color}; font-weight:bold">{completitud}%</td>
                <td>{int(row['duplicados'])}</td>
                <td>{fuera_str}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Calidad - ConAIgua</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        h1 {{ color: #2c3e50; }}
        .summary {{ display: flex; gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); flex: 1; text-align: center; }}
        .card h2 {{ margin: 0; font-size: 2em; color: #2c3e50; }}
        .card p {{ margin: 5px 0 0; color: #7f8c8d; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        th {{ background: #2c3e50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #ecf0f1; }}
        tr:hover {{ background: #f8f9fa; }}
        .timestamp {{ color: #7f8c8d; font-size: 0.9em; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>Reporte de Calidad de Datos - ConAIgua</h1>
    <p class="timestamp">Generado: {timestamp}</p>

    <div class="summary">
        <div class="card">
            <h2>{total_registros:,}</h2>
            <p>Total de registros</p>
        </div>
        <div class="card">
            <h2>{completitud_global}%</h2>
            <p>Completitud global</p>
        </div>
        <div class="card">
            <h2>{duplicados_totales:,}</h2>
            <p>Registros duplicados</p>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Columna</th>
                <th>Tipo</th>
                <th>Nulos</th>
                <th>No nulos</th>
                <th>% Nulos</th>
                <th>Completitud</th>
                <th>Duplicados</th>
                <th>Fuera de rango</th>
            </tr>
        </thead>
        <tbody>
            {filas}
        </tbody>
    </table>
</body>
</html>"""

        path.write_text(html, encoding="utf-8")