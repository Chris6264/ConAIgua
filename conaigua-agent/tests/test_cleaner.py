import pandas as pd
from conaigua.data_pipeline.dataset_cleaner import DataFrameCleaner


def test_replace_nulo():
    df = pd.DataFrame({"precip": ["Nulo"]})

    df_clean = DataFrameCleaner.clean_dataframe(df)

    assert df_clean["precip"].iloc[0] == 0


def test_date_columns():
    df = pd.DataFrame({
        "fecha": ["01/01/2020"]
    })

    df_clean = DataFrameCleaner.clean_dataframe(df)

    assert "anio" in df_clean.columns
    assert "mes" in df_clean.columns
    assert "dia" in df_clean.columns


def test_numeric_conversion():
    df = pd.DataFrame({
        "precip": ["10"],
        "evap": ["5"],
        "tmax": ["25"],
        "tmin": ["15"]
    })

    df_clean = DataFrameCleaner.clean_dataframe(df)

    assert df_clean["precip"].dtype != object


def test_remove_invalid_precip():
    df = pd.DataFrame({
        "precip": [-10],
        "tmax": [25],
        "tmin": [10]
    })

    df_clean = DataFrameCleaner.clean_dataframe(df)

    assert len(df_clean) == 0


def test_temperature_range():
    df = pd.DataFrame({
        "precip": [10],
        "tmax": [100],
        "tmin": [-100]
    })

    df_clean = DataFrameCleaner.clean_dataframe(df)

    assert len(df_clean) == 0


def test_remove_duplicates():
    df = pd.DataFrame({
        "precip": [10, 10],
        "tmax": [25, 25],
        "tmin": [15, 15]
    })

    df_clean = DataFrameCleaner.clean_dataframe(df)

    assert len(df_clean) == 1