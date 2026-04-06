from pathlib import Path
import re

class Parser:

    RAW_DIR = Path(__file__).parent.parent.parent / 'data' / 'raw'
    OUT_FILE = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'conAIgua_dataframe.parquet'
    
    @staticmethod
    def parse_station(filepath: Path) -> list[dict]:
        with open(filepath, 'r', encoding="latin-1", errors='ignore') as f:
            lines = f.readlines()

        meta = {
            "estacion_id": None,
            "nombre_estacion": None,
            "estado": None,
            "municipio": None,
            "situacion_estacion": None,
            "organismo": None,
            "cve_omm": None,
            "latitud": None,
            "longitud": None,
            "altitud_msnm": None
        }

        records = []
        data_started = False

        for line in lines:
            line = line.rstrip()

            if line.startswith("ESTACION"):
                meta["estacion_id"] = line.split(":")[-1].strip()

            elif line.startswith("NOMBRE"):
                meta["nombre_estacion"] = line.split(":")[-1].strip()

            elif line.startswith("ESTADO"):
                meta["estado"] = line.split(":")[-1].strip()

            elif line.startswith("MUNICIPIO"):
                meta["municipio"] = line.split(":")[-1].strip()

            elif "SITUAC" in line and ":" in line:
                meta["situacion_estacion"] = line.split(":")[-1].strip()

            elif line.startswith("ORGANISMO"):
                meta["organismo"] = line.split(":")[-1].strip()

            elif line.startswith("CVE-OMM"):
                meta["cve_omm"] = line.split(":")[-1].strip()

            elif line.startswith("LATITUD"):
                meta["latitud"] = line.split(":")[-1].strip()

            elif line.startswith("LONGITUD"):
                meta["longitud"] = line.split(":")[-1].strip()

            elif line.startswith("ALTITUD"):
                meta["altitud_msnm"] = line.split(":")[-1].strip()

            if line.strip().startswith("FECHA"):
                data_started = True
                continue

            if data_started:
                parts = re.split(r"\s+", line.strip())

                if len(parts) >= 5 and re.match(r"\d{2}/\d{2}/\d{4}", parts[0]):
                    records.append({
                        **meta.copy(),
                        "fecha": parts[0],
                        "precip": parts[1],
                        "evap": parts[2],
                        "tmax": parts[3],
                        "tmin": parts[4],
                    })

        return records