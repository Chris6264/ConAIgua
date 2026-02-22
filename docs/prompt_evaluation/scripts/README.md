# Scripts de Evaluación — PromptBook v1

## 1. Objetivo
Estos scripts permiten evaluar de forma **reproducible** la calidad de prompts bajo las métricas:
- **Estabilidad**: consistencia entre ejecuciones repetidas
- **Precisión (estructural)**: validación del formato JSON y reglas básicas

> Nota: Los scripts NO ejecutan un LLM. Evalúan **salidas ya generadas** (outputs),
> lo cual garantiza reproducibilidad y permite comparar modelos/versiones.

---

## 2. Requisitos
- Python 3.9+

---

## 3. Archivos de ejemplo
- `runs_P-01.json`: entradas/salidas de ejemplo (10 ejecuciones)
- `out_P-01_stability.json`: resultado de estabilidad
- `out_P-01_validation.json`: resultado de validación estructural

---

## 4. Evaluación de Estabilidad (TKT: estabilidad)

### Ejecutar
```bash
python3 docs/evaluacion_prompts/scripts/stability_eval.py \
  --input docs/evaluacion_prompts/scripts/runs_P-01.json \
  --required_sections "estacion_id|municipio|estado|año|precipitacion_total_mm|dias_con_registro|cobertura_datos" \
  --out docs/evaluacion_prompts/scripts/out_P-01_stability.json
