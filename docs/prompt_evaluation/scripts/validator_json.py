#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from typing import Any, Dict, List, Tuple

P01_REQUIRED_KEYS = [
    "estacion_id",
    "nombre_estacion",
    "municipio",
    "estado",
    "situacion_estacion",
    "año",
    "precipitacion_total_mm",
    "dias_con_registro",
    "cobertura_datos",
    "metodo_calculo",
    "notas",
]

P01_METODO_CALCULO_EXPECTED = "Suma anual de registros diarios oficiales CONAGUA"

NUMERIC_FIELDS = [
    "precipitacion_total_mm",
    "dias_con_registro",
]

PERCENT_FIELDS = [
    "cobertura_datos",
]

def is_json_object(s: str) -> Tuple[bool, Dict[str, Any] | None, str]:
    try:
        obj = json.loads(s)
        if isinstance(obj, dict):
            return True, obj, ""
        return False, None, "La salida es JSON pero no es un objeto (dict)."
    except Exception as e:
        return False, None, f"No es JSON válido: {e}"

def has_no_extra_keys(obj: Dict[str, Any], required: List[str]) -> Tuple[bool, List[str]]:
    extra = [k for k in obj.keys() if k not in required]
    return len(extra) == 0, extra

def has_all_required_keys(obj: Dict[str, Any], required: List[str]) -> Tuple[bool, List[str]]:
    missing = [k for k in required if k not in obj]
    return len(missing) == 0, missing

def contains_literal_nulo(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str) and value.strip().lower() == "nulo":
        return True
    return False

def numeric_heuristic_ok(value: Any) -> bool:
    """
    Acepta:
      - número (int/float)
      - string numérica ("842.3", "360")
      - string con % solo en cobertura_datos se maneja aparte
    Rechaza "Nulo" y strings vacías
    """
    if value is None:
        return False
    if contains_literal_nulo(value):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return False
        # acepta "842.3"
        return bool(re.match(r"^-?\d+(\.\d+)?$", s))
    return False

def percent_heuristic_ok(value: Any) -> bool:
    if value is None:
        return False
    if contains_literal_nulo(value):
        return False
    if isinstance(value, str):
        s = value.strip()
        # acepta "98.6%" o "98.6"
        if s.endswith("%"):
            s = s[:-1].strip()
        return bool(re.match(r"^\d+(\.\d+)?$", s))
    if isinstance(value, (int, float)):
        return True
    return False

def validate_p01(obj: Dict[str, Any]) -> Dict[str, Any]:
    ok_required, missing = has_all_required_keys(obj, P01_REQUIRED_KEYS)
    ok_extra, extra = has_no_extra_keys(obj, P01_REQUIRED_KEYS)

    metodo_ok = True
    metodo_note = ""
    if "metodo_calculo" in obj:
        if str(obj["metodo_calculo"]).strip() != P01_METODO_CALCULO_EXPECTED:
            metodo_ok = False
            metodo_note = f"metodo_calculo esperado: '{P01_METODO_CALCULO_EXPECTED}'"

    numeric_issues = []
    for f in NUMERIC_FIELDS:
        if f in obj and not numeric_heuristic_ok(obj[f]):
            numeric_issues.append(f)

    percent_issues = []
    for f in PERCENT_FIELDS:
        if f in obj and not percent_heuristic_ok(obj[f]):
            percent_issues.append(f)

    # Score de precisión estructural (0..5) simple:
    # -5 si todo OK, penaliza por faltantes/extras/errores críticos
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

    if score < 0:
        score = 0.0

    return {
        "schema": "P-01",
        "required_keys_ok": ok_required,
        "missing_required_keys": missing,
        "no_extra_keys_ok": ok_extra,
        "extra_keys": extra,
        "metodo_calculo_ok": metodo_ok,
        "metodo_calculo_note": metodo_note,
        "numeric_fields_issues": numeric_issues,
        "percent_fields_issues": percent_issues,
        "precision_structural_score_0_5": round(score, 2),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="JSON con outputs (runs_*.json)")
    ap.add_argument("--schema", required=True, choices=["P-01"], help="Schema a validar")
    ap.add_argument("--out", default="", help="Ruta salida JSON (opcional)")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    outputs = payload.get("outputs", [])
    if not isinstance(outputs, list) or len(outputs) < 1:
        raise SystemExit("Se requiere al menos 1 output para validar.")

    per_run = []
    json_parse_failures = 0

    for idx, out in enumerate(outputs, start=1):
        ok, obj, err = is_json_object(out)
        if not ok or obj is None:
            json_parse_failures += 1
            per_run.append({
                "run": idx,
                "json_ok": False,
                "error": err
            })
            continue

        if args.schema == "P-01":
            v = validate_p01(obj)
        else:
            v = {"error": "Schema no implementado"}

        per_run.append({
            "run": idx,
            "json_ok": True,
            "validation": v
        })

    # resumen global
    scores = [
        r["validation"]["precision_structural_score_0_5"]
        for r in per_run
        if r.get("json_ok") and "validation" in r and "precision_structural_score_0_5" in r["validation"]
    ]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    result = {
        "prompt_id": payload.get("prompt_id", ""),
        "prompt_version": payload.get("prompt_version", ""),
        "model_id": payload.get("model_id", ""),
        "runs": payload.get("runs", len(outputs)),
        "schema": args.schema,
        "json_parse_failures": json_parse_failures,
        "avg_precision_structural_score_0_5": avg_score,
        "per_run": per_run,
        "notes": "Validación estructural; no valida cálculos numéricos reales (solo forma y reglas básicas)."
    }

    out_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out_json + "\n")
    else:
        print(out_json)

if __name__ == "__main__":
    main()
