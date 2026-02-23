#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from typing import Any, Dict, List, Tuple

# ──────────────────────────────────────────────
# SCHEMAS: required keys, método esperado, campos numéricos y de porcentaje
# ──────────────────────────────────────────────

SCHEMAS = {
    "P-01": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "precipitacion_total_mm",
            "dias_con_registro", "cobertura_datos", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Suma anual de registros diarios oficiales CONAGUA",
        "numeric_fields": ["precipitacion_total_mm", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-02": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "tmax_promedio_anual_c",
            "dias_con_registro", "cobertura_datos", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Promedio anual de TMAX con registros diarios oficiales CONAGUA",
        "numeric_fields": ["tmax_promedio_anual_c", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-03": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "tmin_promedio_anual_c",
            "dias_con_registro", "cobertura_datos", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Promedio anual de TMIN con registros diarios oficiales CONAGUA",
        "numeric_fields": ["tmin_promedio_anual_c", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-04": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "evap_total_mm",
            "dias_con_registro", "cobertura_datos", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Suma anual de EVAP con registros diarios oficiales CONAGUA",
        "numeric_fields": ["evap_total_mm", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-05": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "precip_max_diaria_mm",
            "fecha_precip_max", "dias_con_registro", "cobertura_datos",
            "metodo_calculo", "notas",
        ],
        "metodo_expected": "Máximo anual de PRECIP a partir de registros diarios oficiales CONAGUA",
        "numeric_fields": ["precip_max_diaria_mm", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-06": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "tmin_min_diaria_c",
            "fecha_tmin_min", "dias_con_registro", "cobertura_datos",
            "metodo_calculo", "notas",
        ],
        "metodo_expected": "Mínimo anual de TMIN a partir de registros diarios oficiales CONAGUA",
        "numeric_fields": ["tmin_min_diaria_c", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-07": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "tmax_max_diaria_c",
            "fecha_tmax_max", "dias_con_registro", "cobertura_datos",
            "metodo_calculo", "notas",
        ],
        "metodo_expected": "Máximo anual de TMAX a partir de registros diarios oficiales CONAGUA",
        "numeric_fields": ["tmax_max_diaria_c", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-08": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "dias_con_lluvia_precip_gt_0",
            "dias_con_registro", "cobertura_datos", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Conteo anual de días con PRECIP > 0 a partir de registros diarios oficiales CONAGUA",
        "numeric_fields": ["dias_con_lluvia_precip_gt_0", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-09": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "precip_promedio_dias_lluviosos_mm",
            "dias_con_lluvia", "dias_con_registro", "cobertura_datos",
            "metodo_calculo", "notas",
        ],
        "metodo_expected": "Promedio anual de PRECIP considerando únicamente días con PRECIP > 0 en registros oficiales CONAGUA",
        "numeric_fields": ["precip_promedio_dias_lluviosos_mm", "dias_con_lluvia", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-10": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "situacion_estacion", "año", "correlacion_pearson_tmax_tmin",
            "dias_con_registro", "cobertura_datos", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Coeficiente de correlación de Pearson entre TMAX y TMIN usando registros diarios oficiales CONAGUA",
        "numeric_fields": ["correlacion_pearson_tmax_tmin", "dias_con_registro"],
        "percent_fields": ["cobertura_datos"],
        "metodo_key": "metodo_calculo",
    },
    "P-11": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "periodo_analizado", "pendiente_mm_por_año", "intercepto",
            "r_cuadrado", "p_valor_pendiente", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Regresión lineal simple (OLS) sobre precipitación anual usando datos oficiales CONAGUA",
        "numeric_fields": ["pendiente_mm_por_año", "intercepto", "r_cuadrado", "p_valor_pendiente"],
        "percent_fields": [],
        "metodo_key": "metodo_calculo",
    },
    "P-12": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "año", "beta_tmax", "beta_tmin", "intercepto",
            "r_cuadrado", "p_valor_global", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Regresión lineal múltiple (OLS) PRECIP ~ TMAX + TMIN usando registros diarios oficiales CONAGUA",
        "numeric_fields": ["beta_tmax", "beta_tmin", "intercepto", "r_cuadrado", "p_valor_global"],
        "percent_fields": [],
        "metodo_key": "metodo_calculo",
    },
    "P-13": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "periodo_analizado", "autocorrelacion_lag1",
            "numero_observaciones", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Coeficiente de autocorrelación lag-1 sobre precipitación anual usando datos oficiales CONAGUA",
        "numeric_fields": ["autocorrelacion_lag1", "numero_observaciones"],
        "percent_fields": [],
        "metodo_key": "metodo_calculo",
    },
    "P-14": {
        "required_keys": [
            "estacion_id", "nombre_estacion", "municipio", "estado",
            "periodo_analizado", "estadistico_tau", "p_valor",
            "significancia", "metodo_calculo", "notas",
        ],
        "metodo_expected": "Prueba no paramétrica de tendencia Mann-Kendall aplicada a precipitación anual con datos oficiales CONAGUA",
        "numeric_fields": ["estadistico_tau", "p_valor"],
        "percent_fields": [],
        "metodo_key": "metodo_calculo",
    },
    "P-15": {
        "required_keys": [
            "estacion_origen", "estacion_destino", "estado",
            "periodo_analizado", "tendencia_origen", "tendencia_destino",
            "coherencia_regional", "metodo_transferencia", "notas",
        ],
        "metodo_expected": "Comparación de pruebas Mann-Kendall entre estaciones usando datos oficiales CONAGUA",
        "numeric_fields": [],
        "percent_fields": [],
        "metodo_key": "metodo_transferencia",
    },
    "P-16": {
        "required_keys": [
            "estacion_id", "estado", "periodo_1", "periodo_2",
            "tendencia_periodo_1", "tendencia_periodo_2",
            "cambio_patron", "metodo_transferencia", "notas",
        ],
        "metodo_expected": "Comparación de pruebas Mann-Kendall entre periodos históricos usando datos oficiales CONAGUA",
        "numeric_fields": [],
        "percent_fields": [],
        "metodo_key": "metodo_transferencia",
    },
    "P-17": {
        "required_keys": [
            "estacion_origen", "estacion_destino", "periodo_analizado",
            "pendiente_origen_mm_por_año", "pendiente_destino_mm_por_año",
            "coherencia_direccion", "diferencia_magnitud_mm_por_año",
            "significancia_destino", "metodo_transferencia", "notas",
        ],
        "metodo_expected": "Aplicación comparativa de regresión lineal simple entre estaciones usando datos oficiales CONAGUA",
        "numeric_fields": [
            "pendiente_origen_mm_por_año",
            "pendiente_destino_mm_por_año",
            "diferencia_magnitud_mm_por_año",
        ],
        "percent_fields": [],
        "metodo_key": "metodo_transferencia",
    },
    "P-18": {
        "required_keys": [
            "estacion_id", "periodo_analizado", "resultado_tecnico_original",
            "explicacion_simplificada", "nivel_confianza",
            "metodo_transferencia", "notas",
        ],
        "metodo_expected": "Traducción técnica a lenguaje no especializado manteniendo resultados oficiales CONAGUA",
        "numeric_fields": [],
        "percent_fields": [],
        "metodo_key": "metodo_transferencia",
    },
    "P-19": {
        "required_keys": [
            "estacion_origen", "estacion_destino", "periodo_analizado",
            "pipeline_transferido", "metricas_replicadas",
            "metricas_no_replicadas", "razon_no_replicadas",
            "comparabilidad_global", "metodo_transferencia", "notas",
        ],
        "metodo_expected": "Transferencia de pipeline analítico entre estaciones usando únicamente datos oficiales CONAGUA",
        "numeric_fields": [],
        "percent_fields": [],
        "metodo_key": "metodo_transferencia",
    },
    "P-20": {
        "required_keys": [
            "estacion_id", "periodo_analizado", "hallazgos_clave",
            "coherencia_metodologica", "robustez_estadistica",
            "limitaciones", "conclusion_ejecutiva", "metodo_sintesis", "notas",
        ],
        "metodo_expected": "Integración estructurada de resultados estadísticos oficiales CONAGUA",
        "numeric_fields": [],
        "percent_fields": [],
        "metodo_key": "metodo_sintesis",
    },
}

VALID_SCHEMAS = list(SCHEMAS.keys())

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def is_json_object(s: str) -> Tuple[bool, Dict[str, Any] | None, str]:
    try:
        obj = json.loads(s)
        if isinstance(obj, dict):
            return True, obj, ""
        return False, None, "La salida es JSON pero no es un objeto (dict)."
    except Exception as e:
        return False, None, f"No es JSON válido: {e}"


def has_all_required_keys(obj: Dict[str, Any], required: List[str]) -> Tuple[bool, List[str]]:
    missing = [k for k in required if k not in obj]
    return len(missing) == 0, missing


def has_no_extra_keys(obj: Dict[str, Any], required: List[str]) -> Tuple[bool, List[str]]:
    extra = [k for k in obj.keys() if k not in required]
    return len(extra) == 0, extra


def contains_literal_nulo(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() == "nulo"


def numeric_heuristic_ok(value: Any) -> bool:
    """Acepta int/float o string numérica. Rechaza 'Nulo' y strings vacías."""
    if value is None or contains_literal_nulo(value):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        s = value.strip()
        return bool(s) and bool(re.match(r"^-?\d+(\.\d+)?$", s))
    return False


def percent_heuristic_ok(value: Any) -> bool:
    """Acepta '98.6%', '98.6' o número. Rechaza 'Nulo'."""
    if value is None or contains_literal_nulo(value):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        s = value.strip().rstrip("%").strip()
        return bool(re.match(r"^\d+(\.\d+)?$", s))
    return False

# ──────────────────────────────────────────────
# VALIDACIÓN GENÉRICA
# ──────────────────────────────────────────────

def validate(obj: Dict[str, Any], schema_id: str) -> Dict[str, Any]:
    cfg = SCHEMAS[schema_id]
    required    = cfg["required_keys"]
    metodo_key  = cfg["metodo_key"]
    metodo_exp  = cfg["metodo_expected"]

    ok_required, missing = has_all_required_keys(obj, required)
    ok_extra,    extra   = has_no_extra_keys(obj, required)

    metodo_ok   = True
    metodo_note = ""
    if metodo_key in obj:
        if str(obj[metodo_key]).strip() != metodo_exp:
            metodo_ok   = False
            metodo_note = f"{metodo_key} esperado: '{metodo_exp}'"

    numeric_issues = [f for f in cfg["numeric_fields"] if f in obj and not numeric_heuristic_ok(obj[f])]
    percent_issues = [f for f in cfg["percent_fields"] if f in obj and not percent_heuristic_ok(obj[f])]

    score = 5.0
    if not ok_required:
        score -= min(2.5, 0.5 * len(missing))
    if not ok_extra:
        score -= min(1.5, 0.3 * len(extra))
    if not metodo_ok:
        score -= 0.5
    if numeric_issues:
        score -= min(1.5, 0.5 * len(numeric_issues))
    if percent_issues:
        score -= min(1.0, 0.5 * len(percent_issues))

    return {
        "schema": schema_id,
        "required_keys_ok": ok_required,
        "missing_required_keys": missing,
        "no_extra_keys_ok": ok_extra,
        "extra_keys": extra,
        "metodo_calculo_ok": metodo_ok,
        "metodo_calculo_note": metodo_note,
        "numeric_fields_issues": numeric_issues,
        "percent_fields_issues": percent_issues,
        "precision_structural_score_0_5": round(max(score, 0.0), 2),
    }

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Validador estructural ConAIgua-LLM-v1")
    ap.add_argument("--input",  required=True, help="JSON con outputs (campo 'outputs': list[str])")
    ap.add_argument("--schema", required=True, choices=VALID_SCHEMAS, help="Schema a validar")
    ap.add_argument("--out",    default="",    help="Ruta de salida JSON (opcional; si se omite imprime stdout)")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    outputs = payload.get("outputs", [])
    if not isinstance(outputs, list) or len(outputs) < 1:
        raise SystemExit("Error: se requiere al menos 1 output en el campo 'outputs'.")

    per_run = []
    json_parse_failures = 0

    for idx, out in enumerate(outputs, start=1):
        ok, obj, err = is_json_object(out)
        if not ok or obj is None:
            json_parse_failures += 1
            per_run.append({"run": idx, "json_ok": False, "error": err})
            continue
        per_run.append({"run": idx, "json_ok": True, "validation": validate(obj, args.schema)})

    scores = [
        r["validation"]["precision_structural_score_0_5"]
        for r in per_run
        if r.get("json_ok") and "validation" in r
    ]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    result = {
        "prompt_id":   payload.get("prompt_id", ""),
        "prompt_version": payload.get("prompt_version", ""),
        "model_id":    payload.get("model_id", ""),
        "runs":        payload.get("runs", len(outputs)),
        "schema":      args.schema,
        "json_parse_failures": json_parse_failures,
        "avg_precision_structural_score_0_5": avg_score,
        "per_run": per_run,
        "notes": "Validación estructural; no valida cálculos numéricos reales (solo forma y reglas básicas).",
    }

    out_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out_json + "\n")
        print(f"Resultado guardado en: {args.out}")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
