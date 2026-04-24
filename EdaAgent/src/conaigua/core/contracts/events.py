from enum import Enum


class EventType(str, Enum):
    INGESTA_INICIADA = "ingesta_iniciada"
    INGESTA_COMPLETADA = "ingesta_completada"

    VALIDACION_INICIADA = "validacion_iniciada"
    VALIDACION_COMPLETADA = "validacion_completada"

    PREPROCESAMIENTO_COMPLETADO = "preprocesamiento_completado"

    ANALISIS_INICIADO = "analisis_iniciado"
    ANALISIS_GENERADO = "analisis_generado"

    REPORTE_GENERADO = "reporte_generado"

    PIPELINE_FINALIZADO = "pipeline_finalizado"
    ERROR_DETECTADO = "error_detectado"


class EventStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"