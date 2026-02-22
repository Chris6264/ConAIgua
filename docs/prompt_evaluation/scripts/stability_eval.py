#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from itertools import combinations
from statistics import mean

WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+", re.UNICODE)

def tokenize(text: str) -> set[str]:
    return set(m.group(0).lower() for m in WORD_RE.finditer(text))

def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0

def extract_headings(text: str) -> list[str]:
    headings = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            headings.append(s.lstrip("#").strip().lower())
        elif re.match(r"^(\d+[\.\)]|[IVXLC]+\.)\s+", s):
            headings.append(re.sub(r"^(\d+[\.\)]|[IVXLC]+\.)\s+", "", s).strip().lower())
    return headings

def heading_overlap(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb) if (sa | sb) else 0.0

def stability_score(avg_sim: float, min_sim: float, avg_heading: float) -> float:
    raw = 0.7 * avg_sim + 0.2 * min_sim + 0.1 * avg_heading
    return round(raw * 5.0, 2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Ruta JSON con outputs")
    ap.add_argument("--required_sections", default="", help="Secciones requeridas separadas por '|'")
    ap.add_argument("--out", default="", help="Ruta salida JSON (opcional)")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    outputs = payload.get("outputs", [])
    if not isinstance(outputs, list) or len(outputs) < 2:
        raise SystemExit("Se requieren al menos 2 outputs para evaluar estabilidad.")

    token_sets = [tokenize(o) for o in outputs]
    heading_lists = [extract_headings(o) for o in outputs]

    pair_sims = []
    pair_heads = []
    for i, j in combinations(range(len(outputs)), 2):
        pair_sims.append(jaccard(token_sets[i], token_sets[j]))
        pair_heads.append(heading_overlap(heading_lists[i], heading_lists[j]))

    avg_sim = mean(pair_sims)
    min_sim = min(pair_sims)
    avg_head = mean(pair_heads)

    missing = []
    if args.required_sections.strip():
        req = [r.strip().lower() for r in args.required_sections.split("|") if r.strip()]
        for section in req:
            present_in_all = True
            for out in outputs:
                if section not in out.lower():
                    present_in_all = False
                    break
            if not present_in_all:
                missing.append(section)

    score_0_5 = stability_score(avg_sim, min_sim, avg_head)

    result = {
        "prompt_id": payload.get("prompt_id", ""),
        "prompt_version": payload.get("prompt_version", ""),
        "model_id": payload.get("model_id", ""),
        "runs": payload.get("runs", len(outputs)),
        "similarity": {
            "pairwise_avg_jaccard": round(avg_sim, 4),
            "pairwise_min_jaccard": round(min_sim, 4),
        },
        "structure": {
            "avg_heading_overlap": round(avg_head, 4),
            "missing_required_sections": missing,
        },
        "stability_score_0_5": score_0_5,
        "notes": "Jaccard token-level (proxy semántico) + overlap de headings (proxy estructural).",
    }

    out_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out_json + "\n")
    else:
        print(out_json)

if __name__ == "__main__":
    main()
