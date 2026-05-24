from dataclasses import dataclass, asdict
from typing import Any, Optional


@dataclass
class ErrorInfo:
    codigo: str
    mensaje: str
    detalle: Optional[Any] = None

    def to_dict(self) -> dict:
        return asdict(self)