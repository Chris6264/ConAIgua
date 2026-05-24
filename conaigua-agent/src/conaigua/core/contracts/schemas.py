REQUIRED_MESSAGE_FIELDS = {
    "id_proceso",
    "timestamp",
    "origen",
    "destino",
    "tipo_evento",
    "estado",
    "payload",
    "error",
}


def validate_message_structure(message: dict) -> bool:
    return REQUIRED_MESSAGE_FIELDS.issubset(message.keys())