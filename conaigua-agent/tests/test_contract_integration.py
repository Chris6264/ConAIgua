from conaigua.core.contracts import EventMessage, EventStatus, EventType


def test_pipeline_event_sequence():
    process_id = "proc-integration-001"

    msg1 = EventMessage.create(
        id_proceso=process_id,
        origen="scripts",
        destino="data_pipeline",
        tipo_evento=EventType.INGESTA_INICIADA,
        estado=EventStatus.IN_PROGRESS,
        payload={"archivo_entrada": "data/raw/test.csv"},
    )

    msg2 = EventMessage.create(
        id_proceso=process_id,
        origen="data_pipeline",
        destino="eda_engine",
        tipo_evento=EventType.PREPROCESAMIENTO_COMPLETADO,
        estado=EventStatus.SUCCESS,
        payload={"archivo_salida": "data/processed/test.parquet"},
    )

    assert msg1.id_proceso == msg2.id_proceso
    assert msg1.tipo_evento == "ingesta_iniciada"
    assert msg2.tipo_evento == "preprocesamiento_completado"