from eda_engine.data_loader import load_dataset, filter_data
from eda_engine.eda_pipeline import run_eda

df = load_dataset()

df_filtered = filter_data(df, estacion_id='25001', anio=1978)

result = run_eda(df_filtered,"precip")

import json
print(json.dumps(result, indent = 2, ensure_ascii=False))