import argparse
import json

from conaigua.orchestration.e2e_runner import E2EPipelineRunner


def main():
    parser = argparse.ArgumentParser(description="Ejecuta flujo E2E de ConAIgua")
    parser.add_argument("--station-id", type=str, default=None, help="ID de estación")
    parser.add_argument("--fecha-inicio", type=str, default=None, help="Fecha inicial YYYY-MM-DD")
    parser.add_argument("--fecha-fin", type=str, default=None, help="Fecha final YYYY-MM-DD")

    args = parser.parse_args()

    result = E2EPipelineRunner.run(
        station_id=args.station_id,
        fecha_inicio=args.fecha_inicio,
        fecha_fin=args.fecha_fin,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()