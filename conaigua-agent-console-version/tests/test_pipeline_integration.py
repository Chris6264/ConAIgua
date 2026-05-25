import pandas as pd
from conaigua.data_pipeline.parser import Parser
from conaigua.data_pipeline.dataset_cleaner import DataFrameCleaner


def test_full_pipeline(sample_txt):

    records = Parser.parse_station(sample_txt)
    df = pd.DataFrame(records)

    df_clean = DataFrameCleaner.clean_dataframe(df)

    assert len(df_clean) > 0
    assert "anio" in df_clean.columns
    assert df_clean["precip"].min() >= 0