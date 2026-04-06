import pandas as pd
from conaigua.data_pipeline.quality_report import QualityReport


def test_generate_report_structure():
    df = pd.DataFrame({
        "a": [1, None],
        "b": [None, 2]
    })

    report = QualityReport.generate(df)

    assert "columna" in report.columns
    assert "nulos" in report.columns
    assert "porcentaje_nulos" in report.columns


def test_null_counts():
    df = pd.DataFrame({
        "a": [1, None, None]
    })

    report = QualityReport.generate(df)

    assert report.loc[0, "nulos"] == 2