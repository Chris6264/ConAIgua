from pathlib import Path
from conaigua.eda_engine.data_loader import load_dataset
from conaigua.eda_engine.run_eda_pipeline import run_eda

REPORTS_DIR = Path("reports/eda/markdown")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_station_markdown_report(estacion_id: str):
    df = load_dataset()
    df_station = df[df["estacion_id"] == str(estacion_id)]

    if df_station.empty:
        print(f"No hay datos para la estación {estacion_id}")
        return

    variables = ["precip", "evap", "tmax", "tmin"]
    output_file = REPORTS_DIR / f"eda_station_{estacion_id}.md"
    lines = [f"# Reporte EDA Completo - Estación {estacion_id}\n"]

    for variable in variables:
        result = run_eda(df_station, variable)

        if not result or not result["estadisticos"]:
            lines.append(f"## {variable}\nNo hay datos suficientes.\n")
            continue

        stats = result["estadisticos"]
        outliers = result["outliers"]
        seasonality = result["estacionalidad"]

        lines.append(f"## Variable: {variable}\n")
        lines.append(f"- Media: {stats['media']}")
        lines.append(f"- Mediana: {stats['mediana']}")
        lines.append(f"- Desviación estándar: {stats['desviacion_estandar']}")
        lines.append(f"- Mínimo: {stats['min']}")
        lines.append(f"- Máximo: {stats['max']}")
        lines.append(f"- Conteo válido: {stats['conteo_valido']}")
        lines.append(f"- Outliers detectados: {outliers['cantidad']}")
        lines.append(f"- Mes máximo: {seasonality['mes_maximo'] if seasonality else 'N/A'}")
        lines.append(f"- Mes mínimo: {seasonality['mes_minimo'] if seasonality else 'N/A'}\n")

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Reporte Markdown generado en: {output_file}")