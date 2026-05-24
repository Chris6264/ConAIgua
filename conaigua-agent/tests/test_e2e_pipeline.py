import pandas as pd

from conaigua.orchestration.e2e_runner import E2EPipelineRunner


def test_filter_dataframe_by_station():
    df = pd.DataFrame({
        "station_id": ["25019", "25036", "25019"],
        "fecha": ["2020-01-01", "2020-01-02", "2020-01-03"],
        "precip": [10, 20, 30],
    })

    filtered = E2EPipelineRunner._filter_dataframe(df, station_id="25019")

    assert len(filtered) == 2
    assert all(filtered["station_id"].astype(str) == "25019")


def test_filter_dataframe_by_dates():
    df = pd.DataFrame({
        "station_id": ["25019", "25019", "25019"],
        "fecha": ["2020-01-01", "2020-02-01", "2020-03-01"],
        "precip": [10, 20, 30],
    })

    filtered = E2EPipelineRunner._filter_dataframe(
        df,
        fecha_inicio="2020-01-15",
        fecha_fin="2020-02-15",
    )

    assert len(filtered) == 1
    assert str(filtered.iloc[0]["fecha"].date()) == "2020-02-01"


def test_build_analysis_result_empty_df():
    df = pd.DataFrame(columns=["fecha", "precip", "tmax", "tmin", "evap"])

    result = E2EPipelineRunner._build_analysis_result(
        df,
        station_id="25019",
        fecha_inicio="2020-01-01",
        fecha_fin="2020-12-31",
    )

    assert result["station_id"] == "25019"
    assert result["registros"] == 0
    assert result["resumen"] == {}


def test_build_analysis_result_with_data():
    df = pd.DataFrame({
        "fecha": ["2020-01-01", "2020-01-02"],
        "precip": [10, 20],
        "tmax": [30, 32],
        "tmin": [15, 16],
        "evap": [5, 7],
    })

    result = E2EPipelineRunner._build_analysis_result(df)

    assert result["registros"] == 2
    assert result["resumen"]["precip_media"] == 15.0
    assert result["resumen"]["tmax_media"] == 31.0
    assert result["resumen"]["tmin_media"] == 15.5
    assert result["resumen"]["evap_media"] == 6.0