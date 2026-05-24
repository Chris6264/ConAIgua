from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json
import uuid
import time
import pandas as pd

from conaigua.data_pipeline.pipeline_runner import PipelineRunner
from conaigua.utils.logger import get_e2e_logger
from conaigua.core.contracts import (
    EventMessage,
    EventType,
    EventStatus,
    ErrorInfo,
)


class E2EPipelineRunner:
    BASE_DIR = Path(__file__).resolve().parents[3]
    LOG_DIR = BASE_DIR / "logs"
    EVENTS_FILE = LOG_DIR / "e2e_events.jsonl"

    @classmethod
    def run(
        cls,
        station_id: str | None = None,
        fecha_inicio: str | None = None,
        fecha_fin: str | None = None,
    ) -> dict:
        logger = get_e2e_logger()
        process_id = str(uuid.uuid4())
        start_time = time.time()

        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

        cls._emit_event(
            id_proceso=process_id,
            origen="e2e_runner",
            destino="data_pipeline",
            tipo_evento=EventType.INGESTA_INICIADA,
            estado=EventStatus.IN_PROGRESS,
            payload={
                "station_id": station_id,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
            },
            logger=logger,
        )

        try:
            df = cls._get_or_create_dataset(logger=logger)

            cls._emit_event(
                id_proceso=process_id,
                origen="data_pipeline",
                destino="analysis_filter",
                tipo_evento=EventType.PREPROCESAMIENTO_COMPLETADO,
                estado=EventStatus.SUCCESS,
                payload={
                    "dataset_origen": str(PipelineRunner.OUTPUT_FILE),
                    "registros_totales": len(df),
                },
                logger=logger,
            )

            df_filtrado = cls._filter_dataframe(
                df=df,
                station_id=station_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
            )

            cls._emit_event(
                id_proceso=process_id,
                origen="analysis_filter",
                destino="analysis_engine",
                tipo_evento=EventType.ANALISIS_INICIADO,
                estado=EventStatus.IN_PROGRESS,
                payload={
                    "station_id": station_id,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin,
                    "registros_filtrados": len(df_filtrado),
                },
                logger=logger,
            )

            analysis_result = cls._build_analysis_result(
                df=df_filtrado,
                station_id=station_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
            )

            duration = round(time.time() - start_time, 3)

            cls._emit_event(
                id_proceso=process_id,
                origen="analysis_engine",
                destino="e2e_runner",
                tipo_evento=EventType.ANALISIS_GENERADO,
                estado=EventStatus.SUCCESS,
                payload={
                    "registros_filtrados": len(df_filtrado),
                    "duration_secs": duration,
                },
                logger=logger,
            )

            cls._emit_event(
                id_proceso=process_id,
                origen="e2e_runner",
                destino="pipeline_metrics",
                tipo_evento=EventType.PIPELINE_FINALIZADO,
                estado=EventStatus.SUCCESS,
                payload={
                    "station_id": station_id,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin,
                    "duration_secs": duration,
                },
                logger=logger,
            )

            return {
                "id_proceso": process_id,
                "status": "success",
                "duration_secs": duration,
                "result": analysis_result,
            }

        except Exception as exc:
            error = ErrorInfo(
                codigo="E2E_001",
                mensaje="Error durante la ejecución del flujo E2E",
                detalle=str(exc),
            )

            cls._emit_event(
                id_proceso=process_id,
                origen="e2e_runner",
                destino="e2e_pipeline",
                tipo_evento=EventType.ERROR_DETECTADO,
                estado=EventStatus.FAILED,
                error=error,
                logger=logger,
            )

            logger.exception("Error durante la ejecución del flujo E2E")
            raise

    @classmethod
    def _get_or_create_dataset(cls, logger) -> pd.DataFrame:
        if PipelineRunner.OUTPUT_FILE.exists():
            logger.info(f"Usando parquet existente: {PipelineRunner.OUTPUT_FILE}")
            return pd.read_parquet(PipelineRunner.OUTPUT_FILE)

        logger.info("No existe parquet procesado. Ejecutando pipeline base...")
        return PipelineRunner.run()

    @classmethod
    def _filter_dataframe(
        cls,
        df: pd.DataFrame,
        station_id: str | None = None,
        fecha_inicio: str | None = None,
        fecha_fin: str | None = None,
    ) -> pd.DataFrame:
        filtered_df = df.copy()

        station_col_candidates = ["station_id", "id_estacion", "estacion_id"]
        station_col = next((col for col in station_col_candidates if col in filtered_df.columns), None)

        if station_id is not None:
            if station_col is None:
                raise ValueError("No existe una columna de estación en el dataset.")
            filtered_df = filtered_df[filtered_df[station_col].astype(str) == str(station_id)]

        if "fecha" in filtered_df.columns:
            filtered_df["fecha"] = pd.to_datetime(filtered_df["fecha"], errors="coerce")

            if fecha_inicio is not None:
                fecha_inicio_dt = pd.to_datetime(fecha_inicio, errors="raise")
                filtered_df = filtered_df[filtered_df["fecha"] >= fecha_inicio_dt]

            if fecha_fin is not None:
                fecha_fin_dt = pd.to_datetime(fecha_fin, errors="raise")
                filtered_df = filtered_df[filtered_df["fecha"] <= fecha_fin_dt]
        else:
            if fecha_inicio is not None or fecha_fin is not None:
                raise ValueError("No existe la columna 'fecha' para aplicar filtros temporales.")

        return filtered_df

    @classmethod
    def _build_analysis_result(
        cls,
        df: pd.DataFrame,
        station_id: str | None = None,
        fecha_inicio: str | None = None,
        fecha_fin: str | None = None,
    ) -> dict:
        if df.empty:
            return {
                "station_id": station_id,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "registros": 0,
                "rango_fechas": "no disponible",
                "resumen": {},
            }

        result = {
            "station_id": station_id,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "registros": int(len(df)),
            "rango_fechas": cls._get_date_range(df),
            "resumen": {
                "precip_media": cls._safe_mean(df, "precip"),
                "precip_min": cls._safe_min(df, "precip"),
                "precip_max": cls._safe_max(df, "precip"),
                "tmax_media": cls._safe_mean(df, "tmax"),
                "tmin_media": cls._safe_mean(df, "tmin"),
                "evap_media": cls._safe_mean(df, "evap"),
            },
        }

        return result

    @staticmethod
    def _safe_mean(df: pd.DataFrame, column: str):
        if column not in df.columns:
            return None
        series = pd.to_numeric(df[column], errors="coerce").dropna()
        if series.empty:
            return None
        return round(float(series.mean()), 3)

    @staticmethod
    def _safe_min(df: pd.DataFrame, column: str):
        if column not in df.columns:
            return None
        series = pd.to_numeric(df[column], errors="coerce").dropna()
        if series.empty:
            return None
        return round(float(series.min()), 3)

    @staticmethod
    def _safe_max(df: pd.DataFrame, column: str):
        if column not in df.columns:
            return None
        series = pd.to_numeric(df[column], errors="coerce").dropna()
        if series.empty:
            return None
        return round(float(series.max()), 3)

    @staticmethod
    def _get_date_range(df: pd.DataFrame) -> str:
        if "fecha" not in df.columns:
            return "no disponible"

        fechas = pd.to_datetime(df["fecha"], errors="coerce").dropna()
        if fechas.empty:
            return "no disponible"

        return f"{fechas.min().date()} a {fechas.max().date()}"

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

        with open(cls.EVENTS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")

        if logger:
            logger.info(f"[E2E] Evento emitido: {event.tipo_evento} | estado={event.estado}")

        return event.to_dict()