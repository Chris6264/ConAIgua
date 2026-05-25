import json
from pathlib import Path

from conaigua.orchestration.e2e_runner import E2EPipelineRunner
from conaigua.core.contracts import EventType, EventStatus


def test_emit_e2e_event_creates_jsonl(tmp_path, monkeypatch):
    test_events_file = tmp_path / "e2e_events.jsonl"

    monkeypatch.setattr(E2EPipelineRunner, "EVENTS_FILE", test_events_file)
    monkeypatch.setattr(E2EPipelineRunner, "LOG_DIR", tmp_path)

    event = E2EPipelineRunner._emit_event(
        id_proceso="test-process-001",
        origen="e2e_runner",
        destino="analysis_engine",
        tipo_evento=EventType.ANALISIS_INICIADO,
        estado=EventStatus.IN_PROGRESS,
        payload={"station_id": "25019"},
    )

    assert test_events_file.exists()
    assert event["id_proceso"] == "test-process-001"
    assert event["tipo_evento"] == "analisis_iniciado"
    assert event["estado"] == "in_progress"

    lines = test_events_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    saved_event = json.loads(lines[0])

    assert saved_event["id_proceso"] == "test-process-001"
    assert saved_event["origen"] == "e2e_runner"
    assert saved_event["destino"] == "analysis_engine"
    assert saved_event["payload"]["station_id"] == "25019"
    assert saved_event["error"] is None