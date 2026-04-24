# Reporte End-to-End

## Objetivo
Validar el flujo completo del sistema ConAIgua.

## Flujo probado
Usuario → agente → tool → E2E → análisis

## Resultados

- Flujo ejecutado correctamente
- Filtrado por estación y fechas funcional
- Resultados consistentes
- Eventos generados correctamente

## Evidencia

Comando:

```bash
pytest tests/integration -v
