import pandas as pd

from conaigua.orchestration.e2e_runner import E2EPipelineRunner


def test_e2e_filter_by_station_and_dates():
    df = pd.DataFrame({
        "station_id": ["25019", "25019", "25036"],
        "fecha": ["1978-01-01", "1978-12-31", "1978-06-01"],
        "precip": [0.0, 10.0, 20.0],
        "tmax": [30.0, 35.0, 33.0],
        "tmin": [15.0, 16.0, 18.0],
        "evap": [5.0, 6.0, 7.0],
    })

    filtered = E2EPipelineRunner._filter_dataframe(
        df=df,
        station_id="25019",
        fecha_inicio="1978-01-01",
        fecha_fin="1978-12-31",
    )

    assert len(filtered) == 2
    assert all(filtered["station_id"].astype(str) == "25019")


def test_e2e_analysis_result_is_reproducible():
    df = pd.DataFrame({
        "station_id": ["25019", "25019"],
        "fecha": ["1978-01-01", "1978-01-02"],
        "precip": [0.0, 10.0],
        "tmax": [30.0, 34.0],
        "tmin": [15.0, 17.0],
        "evap": [5.0, 7.0],
    })

    result = E2EPipelineRunner._build_analysis_result(
        df=df,
        station_id="25019",
        fecha_inicio="1978-01-01",
        fecha_fin="1978-01-02",
    )

    assert result["station_id"] == "25019"
    assert result["registros"] == 2
    assert result["rango_fechas"] == "1978-01-01 a 1978-01-02"
    assert result["resumen"]["precip_media"] == 5.0
    assert result["resumen"]["tmax_media"] == 32.0
    assert result["resumen"]["tmin_media"] == 16.0
    assert result["resumen"]["evap_media"] == 6.0


def test_e2e_empty_result():
    df = pd.DataFrame(columns=[
        "station_id",
        "fecha",
        "precip",
        "tmax",
        "tmin",
        "evap",
    ])

    result = E2EPipelineRunner._build_analysis_result(
        df=df,
        station_id="25019",
        fecha_inicio="1900-01-01",
        fecha_fin="1900-12-31",
    )

    assert result["registros"] == 0
    assert result["rango_fechas"] == "no disponible"
    assert result["resumen"] == {}