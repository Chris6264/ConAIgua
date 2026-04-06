from pathlib import Path
import pandas as pd

from conaigua.data_pipeline.parser import Parser
from conaigua.data_pipeline.dataset_cleaner import DataFrameCleaner
from conaigua.data_pipeline.quality_report import QualityReport


class PipelineRunner:

    BASE_DIR = Path(__file__).resolve().parents[3]
    RAW_DIR = BASE_DIR / "data" / "raw"
    PROCESSED_DIR = BASE_DIR / "data" / "processed"

    OUTPUT_FILE = PROCESSED_DIR / "conAIgua_dataframe.parquet"
    QUALITY_FILE = PROCESSED_DIR / "quality_report.csv"

    @classmethod
    def run(cls) -> pd.DataFrame:
        print("Iniciando pipeline de datos...")

        cls._ensure_dirs()

        all_records = []

        files = list(cls.RAW_DIR.glob("*.txt"))
        if not files:
            raise FileNotFoundError(f"No se encontraron archivos en {cls.RAW_DIR}")

        print(f"Archivos encontrados: {len(files)}")

        for file in files:
            print(f"Procesando: {file.name}")
            records = Parser.parse_station(file)
            all_records.extend(records)

        if not all_records:
            raise ValueError("No se generaron registros")

        df = pd.DataFrame(all_records)
        print(f"Registros totales: {len(df)}")

        df = DataFrameCleaner.clean_dataframe(df)
        print(f"Registros después de limpieza: {len(df)}")

        df.to_parquet(cls.OUTPUT_FILE, index=False)
        print(f"Archivo guardado en: {cls.OUTPUT_FILE}")

        report = QualityReport.generate(df)
        QualityReport.save(report, cls.QUALITY_FILE)
        print(f"Reporte de calidad guardado en: {cls.QUALITY_FILE}")

        print("Pipeline finalizado correctamente")

        return df

    @classmethod
    def _ensure_dirs(cls):
        cls.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def run_data_pipeline():
    return PipelineRunner.run()