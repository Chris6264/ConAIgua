from pathlib import Path
import pandas as pd
from ydata_profiling import ProfileReport

from scripts.eda_engine.data_loader import load_dataset

REPORTS_DIR = Path('reports/eda/html')
REPORTS_DIR.mkdir(parents=True, exist_ok= True)

def generate_station_html_report(estacion_id : str):
    
    df = load_dataset()
    df_station = df[df['estacion_id'] == str(estacion_id)]
    
    if df_station.empty:
        print(f'No hay datos de la estación {estacion_id}')
        return
    
    profile = ProfileReport(
        df_station,
        title = f'Reporte EDA - Estación {estacion_id}',
        explorative= True
    )
    
    output_file = REPORTS_DIR / f'eda_station_{estacion_id}.html'
    profile.to_file(output_file)
    
    print(f"Reporte html generado en: {output_file}")