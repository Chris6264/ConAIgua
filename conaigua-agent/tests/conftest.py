import pytest
from pathlib import Path


@pytest.fixture
def sample_txt(tmp_path: Path):
    file = tmp_path / "station_test.txt"

    file.write_text(
        """ESTACION: 001
NOMBRE: TEST_STATION
ESTADO: SINALOA
MUNICIPIO: CULIACAN
SITUACION: OPERANDO
ORGANISMO: CONAGUA
CVE-OMM: 12345
LATITUD: 24.80
LONGITUD: -107.39
ALTITUD: 50

FECHA PRECIP EVAP TMAX TMIN
01/01/2020 10 5 25 15
02/01/2020 -5 3 100 -60
03/01/2020 Nulo 2 30 20
""",
        encoding="latin-1"
    )

    return file


@pytest.fixture
def mock_config():
    return {
        "llm": {
            "provider": "groq",
            "model": "llama-3.3-70b-versatile",
            "api_key": "fake-key"
        }
    }