from pathlib import Path
from datetime import datetime
import json
import time
import pandas as pd

from conaigua.data_pipeline.parser import Parser
from conaigua.data_pipeline.dataset_cleaner import DataFrameCleaner
from conaigua.data_pipeline.quality_report import QualityReport
from conaigua.utils.logger import get_pipeline_logger


class PipelineRunner:

    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    RAW_DIR = BASE_DIR / "data" / "raw"
    PROCESSED_DIR = BASE_DIR / "data" / "processed"
    LOG_DIR = BASE_DIR / "logs"
    METRICS_FILE = LOG_DIR / "metrics.json"

    OUTPUT_FILE = PROCESSED_DIR / "conAIgua_dataframe.parquet"
    QUALITY_FILE = PROCESSED_DIR / "quality_report.csv"

    @classmethod
    def run(cls) -> pd.DataFrame:
        logger = get_pipeline_logger()
        start_time = time.time()
        timestamp = datetime.now().isoformat()

        logger.info("Iniciando pipeline de datos...")

        cls._ensure_dirs()

        all_records = []

        files = list(cls.RAW_DIR.glob("*.txt"))
        if not files:
            logger.error(f"No se encontraron archivos en {cls.RAW_DIR}")
            raise FileNotFoundError(f"No se encontraron archivos en {cls.RAW_DIR}")

        logger.info(f"Archivos encontrados: {len(files)}")

        for file in files:
            logger.info(f"Procesando: {file.name}")
            records = Parser.parse_station(file)
            all_records.extend(records)

        if not all_records:
            logger.error("No se generaron registros")
            raise ValueError("No se generaron registros")

        df = pd.DataFrame(all_records)
        logger.info(f"Registros totales: {len(df)}")

        df = DataFrameCleaner.clean_dataframe(df)
        registros_limpios = len(df)
        logger.info(f"Registros después de limpieza: {registros_limpios}")

        df.to_parquet(cls.OUTPUT_FILE, index=False)
        logger.info(f"Parquet guardado en: {cls.OUTPUT_FILE}")

        report = QualityReport.generate(df)
        QualityReport.save(report, cls.QUALITY_FILE)
        logger.info(f"Reporte de calidad guardado en: {cls.QUALITY_FILE}")

        duration = round(time.time() - start_time, 3)
        logger.info(f"Pipeline finalizado en {duration}s")

        metrics = {
            "timestamp": timestamp,
            "status": "ok",
            "duration_secs": duration,
            "archivos_procesados": len(files),
            "registros_totales": len(df),
            "registros_limpios": registros_limpios,
        }
        cls._save_metrics(metrics, logger)

        return df

    @classmethod
    def _ensure_dirs(cls):
        cls.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _save_metrics(cls, metrics: dict, logger):
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        history = []
        if cls.METRICS_FILE.exists():
            with open(cls.METRICS_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)

        history.append(metrics)

        with open(cls.METRICS_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        logger.info(f"Métricas guardadas en: {cls.METRICS_FILE}")


def run_data_pipeline():
    return PipelineRunner.run()