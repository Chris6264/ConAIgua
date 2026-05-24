from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Optional

from conaigua.core.contracts.errors import ErrorInfo
from conaigua.core.contracts.events import EventType, EventStatus


@dataclass
class EventMessage:
    id_proceso: str
    timestamp: str
    origen: str
    destino: str
    tipo_evento: str
    estado: str
    payload: Optional[Any] = None
    error: Optional[dict] = None

    @staticmethod
    def now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def create(
        cls,
        id_proceso: str,
        origen: str,
        destino: str,
        tipo_evento: EventType,
        estado: EventStatus,
        payload: Optional[Any] = None,
        error: Optional[ErrorInfo] = None,
    ) -> "EventMessage":
        return cls(
            id_proceso=id_proceso,
            timestamp=cls.now(),
            origen=origen,
            destino=destino,
            tipo_evento=tipo_evento.value,
            estado=estado.value,
            payload=payload,
            error=error.to_dict() if error else None,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json_ready(self) -> dict:
        return self.to_dict()