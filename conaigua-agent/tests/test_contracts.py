from conaigua.core.contracts import (
    EventMessage,
    EventStatus,
    EventType,
    ErrorInfo,
    validate_message_structure,
)


def test_create_success_message():
    msg = EventMessage.create(
        id_proceso="proc-001",
        origen="data_pipeline",
        destino="eda_engine",
        tipo_evento=EventType.PREPROCESAMIENTO_COMPLETADO,
        estado=EventStatus.SUCCESS,
        payload={"archivo_salida": "data/processed/output.parquet"},
    )

    data = msg.to_dict()

    assert data["id_proceso"] == "proc-001"
    assert data["origen"] == "data_pipeline"
    assert data["destino"] == "eda_engine"
    assert data["tipo_evento"] == "preprocesamiento_completado"
    assert data["estado"] == "success"
    assert data["payload"]["archivo_salida"] == "data/processed/output.parquet"
    assert data["error"] is None


def test_create_error_message():
    msg = EventMessage.create(
        id_proceso="proc-002",
        origen="validation_service",
        destino="data_pipeline",
        tipo_evento=EventType.ERROR_DETECTADO,
        estado=EventStatus.FAILED,
        error=ErrorInfo(
            codigo="VAL_001",
            mensaje="Columnas requeridas faltantes",
            detalle=["fecha", "latitud"],
        ),
    )

    data = msg.to_dict()

    assert data["estado"] == "failed"
    assert data["tipo_evento"] == "error_detectado"
    assert data["error"]["codigo"] == "VAL_001"
    assert data["error"]["mensaje"] == "Columnas requeridas faltantes"
    assert "fecha" in data["error"]["detalle"]


def test_validate_message_structure():
    msg = EventMessage.create(
        id_proceso="proc-003",
        origen="scripts",
        destino="data_pipeline",
        tipo_evento=EventType.INGESTA_INICIADA,
        estado=EventStatus.IN_PROGRESS,
        payload={"archivo_entrada": "data/raw/input.csv"},
    )

    assert validate_message_structure(msg.to_dict()) is True