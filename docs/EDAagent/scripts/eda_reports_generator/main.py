from eda_engine.data_loader import load_dataset
from scripts.eda_reports_generator.html_generator import generate_station_html_report
from scripts.eda_reports_generator.markdown_generator import generate_station_markdown_report

def main():
    print("Cargando dataset...")
    df = load_dataset()
    estaciones = df['estacion_id'].unique()
    total = len(estaciones)

    print(f"Generando reportes para {total} estaciones...")
    for i, estacion_id in enumerate(estaciones, 1):
        print(f"[{i}/{total}] Estación {estacion_id}...")
        generate_station_html_report(estacion_id)
        generate_station_markdown_report(estacion_id)

    print("Generación de reportes finalizada.")

if __name__ == "__main__":
    main()