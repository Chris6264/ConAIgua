from pathlib import Path
from datetime import datetime
import json
import time
import uuid
import pandas as pd

from conaigua.data_pipeline.parser import Parser
from conaigua.data_pipeline.dataset_cleaner import DataFrameCleaner
from conaigua.data_pipeline.quality_report import QualityReport
from conaigua.utils.logger import get_pipeline_logger

from conaigua.core.contracts import (
    EventMessage,
    EventType,
    EventStatus,
    ErrorInfo,
)


class PipelineRunner:

    BASE_DIR = Path(__file__).resolve().parents[3]
    RAW_DIR = BASE_DIR / "data" / "raw"
    PROCESSED_DIR = BASE_DIR / "data" / "processed"
    LOG_DIR = BASE_DIR / "logs"
    METRICS_FILE = LOG_DIR / "metrics.json"
    EVENTS_FILE = LOG_DIR / "pipeline_events.jsonl"

    OUTPUT_FILE = PROCESSED_DIR / "conAIgua_dataframe.parquet"
    QUALITY_FILE = PROCESSED_DIR / "quality_report.csv"
    QUALITY_HTML = PROCESSED_DIR / "quality_report.html"

    @classmethod
    def run(cls) -> pd.DataFrame:
        logger = get_pipeline_logger()
        start_time = time.time()
        timestamp = datetime.now().isoformat()
        process_id = str(uuid.uuid4())

        print("Iniciando pipeline de datos...")
        logger.info("Iniciando pipeline de datos...")

        cls._ensure_dirs()

        cls._emit_event(
            id_proceso=process_id,
            origen="pipeline_runner",
            destino="data_pipeline",
            tipo_evento=EventType.INGESTA_INICIADA,
            estado=EventStatus.IN_PROGRESS,
            payload={
                "raw_dir": str(cls.RAW_DIR),
                "timestamp": timestamp
            },
            logger=logger,
        )

        try:
            all_records = []

            files = list(cls.RAW_DIR.glob("*.txt"))
            if not files:
                error = ErrorInfo(
                    codigo="PIPE_001",
                    mensaje=f"No se encontraron archivos en {cls.RAW_DIR}",
                    detalle={"raw_dir": str(cls.RAW_DIR)}
                )

                cls._emit_event(
                    id_proceso=process_id,
                    origen="pipeline_runner",
                    destino="data_pipeline",
                    tipo_evento=EventType.ERROR_DETECTADO,
                    estado=EventStatus.FAILED,
                    error=error,
                    logger=logger,
                )

                logger.error(f"No se encontraron archivos en {cls.RAW_DIR}")
                raise FileNotFoundError(f"No se encontraron archivos en {cls.RAW_DIR}")

            logger.info(f"Archivos encontrados: {len(files)}")

            cls._emit_event(
                id_proceso=process_id,
                origen="pipeline_runner",
                destino="parser",
                tipo_evento=EventType.INGESTA_COMPLETADA,
                estado=EventStatus.SUCCESS,
                payload={
                    "archivos_encontrados": len(files),
                    "archivos": [file.name for file in files]
                },
                logger=logger,
            )

            for file in files:
                logger.info(f"Procesando: {file.name}")
                records = Parser.parse_station(file)
                all_records.extend(records)

            if not all_records:
                error = ErrorInfo(
                    codigo="PIPE_002",
                    mensaje="No se generaron registros",
                    detalle=None
                )

                cls._emit_event(
                    id_proceso=process_id,
                    origen="parser",
                    destino="data_pipeline",
                    tipo_evento=EventType.ERROR_DETECTADO,
                    estado=EventStatus.FAILED,
                    error=error,
                    logger=logger,
                )

                logger.error("No se generaron registros")
                raise ValueError("No se generaron registros")

            df = pd.DataFrame(all_records)
            logger.info(f"Registros totales: {len(df)}")

            cls._emit_event(
                id_proceso=process_id,
                origen="parser",
                destino="dataset_cleaner",
                tipo_evento=EventType.VALIDACION_INICIADA,
                estado=EventStatus.IN_PROGRESS,
                payload={"registros_totales": len(df)},
                logger=logger,
            )

            df = DataFrameCleaner.clean_dataframe(df)
            registros_limpios = len(df)
            logger.info(f"Registros después de limpieza: {registros_limpios}")

            cls._emit_event(
                id_proceso=process_id,
                origen="dataset_cleaner",
                destino="processed_storage",
                tipo_evento=EventType.PREPROCESAMIENTO_COMPLETADO,
                estado=EventStatus.SUCCESS,
                payload={
                    "registros_limpios": registros_limpios,
                    "archivo_salida": str(cls.OUTPUT_FILE)
                },
                logger=logger,
            )

            df.to_parquet(cls.OUTPUT_FILE, index=False)
            logger.info(f"Parquet guardado en: {cls.OUTPUT_FILE}")

            report = QualityReport.generate(df)
            QualityReport.save(report, cls.QUALITY_FILE)
            logger.info(f"Reporte CSV guardado en: {cls.QUALITY_FILE}")

            QualityReport.generate_html(report, df, cls.QUALITY_HTML)
            logger.info(f"Reporte HTML guardado en: {cls.QUALITY_HTML}")

            cls._emit_event(
                id_proceso=process_id,
                origen="data_pipeline",
                destino="quality_report",
                tipo_evento=EventType.REPORTE_GENERADO,
                estado=EventStatus.SUCCESS,
                payload={
                    "quality_csv": str(cls.QUALITY_FILE),
                    "quality_html": str(cls.QUALITY_HTML)
                },
                logger=logger,
            )

            duration = round(time.time() - start_time, 3)
            print(f"Pipeline finalizado en {duration}s")
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

            cls._emit_event(
                id_proceso=process_id,
                origen="pipeline_runner",
                destino="pipeline_metrics",
                tipo_evento=EventType.VALIDACION_COMPLETADA,
                estado=EventStatus.SUCCESS,
                payload={
                    "duration_secs": duration,
                    "metrics_file": str(cls.METRICS_FILE)
                },
                logger=logger,
            )

            return df

        except Exception as exc:
            error = ErrorInfo(
                codigo="PIPE_999",
                mensaje="Error durante la ejecución del pipeline",
                detalle=str(exc)
            )

            cls._emit_event(
                id_proceso=process_id,
                origen="pipeline_runner",
                destino="data_pipeline",
                tipo_evento=EventType.ERROR_DETECTADO,
                estado=EventStatus.FAILED,
                error=error,
                logger=logger,
            )

            logger.exception("Error durante la ejecución del pipeline")
            raise

    @classmethod
    def _ensure_dirs(cls):
        cls.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

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

    @classmethod
    def _emit_event(
        cls,
        id_proceso: str,
        origen: str,
        destino: str,
        tipo_evento: EventType,
        estado: EventStatus,
        payload: dict | None = None,
        error: ErrorInfo | None = None,
        logger=None,
    ) -> dict:
        event = EventMessage.create(
            id_proceso=id_proceso,
            origen=origen,
            destino=destino,
            tipo_evento=tipo_evento,
            estado=estado,
            payload=payload,
            error=error,
        )

        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

        with open(cls.EVENTS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")

        if logger:
            logger.info(
                f"Evento emitido: {event.tipo_evento} | estado={event.estado}"
            )

        return event.to_dict()


def run_data_pipeline():
    return PipelineRunner.run()