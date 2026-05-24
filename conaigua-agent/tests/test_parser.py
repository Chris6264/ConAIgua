from conaigua.data_pipeline.parser import Parser

def test_parse_station_returns_records(sample_txt):
    records = Parser.parse_station(sample_txt)

    assert isinstance(records, list)
    assert len(records) == 3


def test_parse_station_contains_metadata(sample_txt):
    records = Parser.parse_station(sample_txt)

    record = records[0]

    assert record["estacion_id"] == "001"
    assert record["nombre_estacion"] == "TEST_STATION"
    assert record["estado"] == "SINALOA"


def test_parse_station_data_fields(sample_txt):
    records = Parser.parse_station(sample_txt)

    record = records[0]

    assert "fecha" in record
    assert "precip" in record
    assert "tmax" in record