from enum import Enum


class EventType(str, Enum):
    INGESTA_INICIADA = "ingesta_iniciada"
    INGESTA_COMPLETADA = "ingesta_completada"

    VALIDACION_INICIADA = "validacion_iniciada"
    VALIDACION_COMPLETADA = "validacion_completada"

    PREPROCESAMIENTO_INICIADO = "preprocesamiento_iniciado"
    PREPROCESAMIENTO_COMPLETADO = "preprocesamiento_completado"

    ANALISIS_INICIADO = "analisis_iniciado"
    ANALISIS_GENERADO = "analisis_generado"

    REPORTE_INICIADO = "reporte_iniciado"
    REPORTE_GENERADO = "reporte_generado"

    ERROR_DETECTADO = "error_detectado"


class EventStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"