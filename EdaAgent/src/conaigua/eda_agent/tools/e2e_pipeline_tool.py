from conaigua.orchestration.e2e_runner import E2EPipelineRunner


def e2e_pipeline_tool(
    station_id: str | None = None,
    fecha_inicio: str | None = None,
    fecha_fin: str | None = None,
):
    """
    Ejecuta flujo E2E de ingesta, limpieza y análisis.

    Args:
        station_id: ID de estación (ej. "25019")
        fecha_inicio: Fecha inicio YYYY-MM-DD
        fecha_fin: Fecha fin YYYY-MM-DD

    Returns:
        Resultado estructurado del análisis
    """
    result = E2EPipelineRunner.run(
        station_id=station_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )

    return result["result"]