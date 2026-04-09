import pandas as pd
from conaigua.data_pipeline.quality_report import QualityReport


def test_generate_report_structure():
    df = pd.DataFrame({
        "a": [1, None],
        "b": [None, 2]
    })

    report = QualityReport.generate(df)

    # Verifica estructura
    assert "columna" in report.columns
    assert "nulos" in report.columns
    assert "porcentaje_nulos" in report.columns


def test_null_counts():
    df = pd.DataFrame({
        "a": [1, None, None]
    })

    report = QualityReport.generate(df).set_index("columna")

    # Verifica cantidad de nulos
    assert report.loc["a", "nulos"] == 2


def test_null_percentage():
    df = pd.DataFrame({
        "a": [1, None, None]
    })

    report = QualityReport.generate(df).set_index("columna")

    # Verifica porcentaje de nulos
    expected = (2 / 3) * 100
    assert report.loc["a", "porcentaje_nulos"] == expected


def test_multiple_columns():
    df = pd.DataFrame({
        "a": [1, None, None],
        "b": [1, 2, 3]
    })

    report = QualityReport.generate(df).set_index("columna")

    # Columna con nulos
    assert report.loc["a", "nulos"] == 2

    # Columna sin nulos
    assert report.loc["b", "nulos"] == 0


def test_empty_dataframe():
    df = pd.DataFrame()

    report = QualityReport.generate(df)

    # Debe devolver DataFrame vacío pero válido
    assert isinstance(report, pd.DataFrame)
    assert report.empty


def test_all_nulls():
    df = pd.DataFrame({
        "a": [None, None],
        "b": [None, None]
    })

    report = QualityReport.generate(df).set_index("columna")

    assert report.loc["a", "nulos"] == 2
    assert report.loc["b", "nulos"] == 2

    assert report.loc["a", "porcentaje_nulos"] == 100.0
    assert report.loc["b", "porcentaje_nulos"] == 100.0