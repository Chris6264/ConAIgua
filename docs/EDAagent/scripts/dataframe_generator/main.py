# main.py
from scripts.dataframe_generator.parser import Parser
from scripts.dataframe_generator.dataframe_cleaner import DataFrameCleaner
import pandas as pd

def main():
    print("Buscando archivos en:", Parser.RAW_DIR)
    print("Archivos encontrados:", list(Parser.RAW_DIR.glob("*")))

    all_records = []
    for filepath in Parser.RAW_DIR.glob("*"):
        if filepath.is_file():
            all_records.extend(Parser.parse_station(filepath))

    print("Total records:", len(all_records))  # debe ser > 0
    
    all_records = []
    for filepath in Parser.RAW_DIR.glob("*"):
        if filepath.is_file():
            all_records.extend(Parser.parse_station(filepath))

    df = pd.DataFrame(all_records)
    df = DataFrameCleaner.clean_dataframe(df)

    Parser.OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(Parser.OUT_FILE, index=False)

    print("Dataset procesado guardado en:", Parser.OUT_FILE)
    print("Filas:", len(df))
    print("Columnas:", list(df.columns))
    print(df.head())

if __name__ == "__main__":
    main()