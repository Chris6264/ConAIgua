# ConAIgua — Hydrometeorological EDA Agent

Conversational agent specialized in the exploratory analysis of hydrometeorological data from CONAGUA stations in Sinaloa, Mexico. It allows querying statistics, correlations, regressions, and generating reports through natural language from the terminal.

---
<div align="center">

[Versión en Español](README.md)

</div>

## Prerequisites

- **Python 3.12** — [download here](https://www.python.org/downloads/)
- **uv** — package manager (see installation below)
- **API Key** from the LLM provider you'll use (see providers section)

### Install uv

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux / Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**With pip (universal alternative):**
```bash
pip install uv
```

> If you prefer not to use `uv`, you can use `pip` directly.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Chris6264/ConAIgua.git
cd EdaAgent
```

### 2. Create the virtual environment with Python 3.12

```bash
uv venv --python 3.12 .venv
```

Without `uv`:
```bash
python -m venv .venv
```

### 3. Activate the virtual environment

```bash
# Windows
.venv\Scripts\Activate.ps1

# Linux / Mac
source .venv/bin/activate
```

### 4. Install dependencies

```bash
uv pip install -e .
```

Without `uv`:
```bash
pip install -e .
```

### 5. Configure environment variables

Copy the example file:

```bash
# Windows
copy .env.example .env

# Linux / Mac
cp .env.example .env
```
Copy the configuration file:

```bash
# Windows
cd config
copy config.example.yaml config.yaml

# Linux / Mac
cd config
cp config.example.yaml config.yaml
```

Open `.env` and configure your provider and API key:

```dotenv
# LLM provider — options: groq, openai, anthropic, google
LLM_PROVIDER="groq"

# Add ONLY the key for the provider you'll use
GROQ_API_KEY="your_api_key_here"
OPENAI_API_KEY="your_api_key_here"
ANTHROPIC_API_KEY="your_api_key_here"
GOOGLE_API_KEY="your_api_key_here"
```

Then, in the `config` directory, open the `config.yaml` file and configure your provider and API key:

```dotenv
llm:
  provider: groq #Set your provider
  model: llama-3.3-70b-versatile #Set your model
  api_key_env: "" #Set your API key as an environment variable name.
  temperature: 0
  max_tokens: 1024
```

### 6. Prepare the dataset

The stations' `.txt` files must be located in `data/raw/`. Once there, generate the processed dataset with the pipeline:

```bash
python -m scripts.run_data_pipeline
```

This will create `data/processed/conAIgua_dataframe.parquet`.

> If you already have the `.parquet` file, you can skip this step.

---

## Running the agent

Once the processed file has been generated, the agent can be run via LangGraph using the following command:

```bash
PYTHONPATH="$PWD/src" uv run langgraph dev
```
Additionally, to view the generated EDA reports in HTML format, you can start a local server from the reports folder using the following commands:

```bash
cd reports/eda 
python -m http.server 8080
```

Press `Ctrl + C` to end the session.

---

## LLM Providers

| Provider | `LLM_PROVIDER` | Get API Key | Free tier |
|-----------|----------------|-----------------|---------------|
| **Groq** (recommended) | `groq` | https://console.groq.com | Yes |
| OpenAI | `openai` | https://platform.openai.com/api-keys | No |
| Anthropic (Claude) | `anthropic` | https://console.anthropic.com | No |
| Google Gemini | `google` | https://aistudio.google.com/app/apikey | Yes |

The default model is `qwen/qwen3-32b` on Groq. You can change it in `scripts/eda_agent/config/llm_wrapper.py` and adjust the level (`rapido`, `balanceado`, `razonamiento`) and temperature in `scripts/eda_agent/config/agent_setup.py`.

---

## Agent capabilities

| Capability | Description |
|-----------|-------------|
| EDA statistics | Mean, median, min, max, std, outliers, and seasonality |
| Correlations | Pearson and Spearman with p-value and statistical significance |
| Regressions | Simple and multiple linear regression with R², RMSE, 95% CI, and diagnostics |
| Trends | Annual trend analysis over year ranges |
| Reports | HTML (ydata-profiling) and Markdown per station |
| Stations | Listing of all available stations |

### Available variables

| Variable | Description | Unit |
|----------|-------------|--------|
| `precip` | Precipitation | mm |
| `evap` | Evaporation | mm |
| `tmax` | Maximum temperature | °C |
| `tmin` | Minimum temperature | °C |
| `mes` | Month of the year | 1–12 |
| `anio` | Year of the record | — |

---

## Usage examples

```
What stations are available?
Give me the average precipitation for station 25001
Give me the average precipitation for station 25001 for the year 1978
What was the correlation between precipitation and maximum temperature at station 25001?
Calculate the linear regression of precipitation against month at station 25001
Do a multiple regression of precipitation against month and year at station 25001
What is the precipitation trend at station 25001 between 1970 and 1980?
Generate a report for station 25001
Generate a report for station 25001 in html
```

---

## Project structure

```
 conaigua-agent/
    ├── config/
    │   ├── config.example.yaml
    │   └── config.yaml
    ├── data/
    │   ├── processed/
    │   └── raw/
    ├── logs/
    │   ├── errors.log
    │   ├── metrics.json
    │   ├── pipeline_events.jsonl
    │   └── pipeline.log
    ├── notebooks/
    │   ├── check_quality_report.ipynb
    │   ├── correlation_check.ipynb
    │   ├── dataframe_check.ipynb
    │   ├── regression_check.ipynb
    │   └── US_3_2_Modelado.ipynb
    ├── reports/
    │   └── eda/
    │       ├── html/
    │       │   ├── eda_station_25078.html
    │       │   ├── eda_station_25161.html
    │       │   └── eda_station_25164.html
    │       └── markdown/
    │           ├── eda_station_25078.md
    │           ├── eda_station_25161.md
    │           └── eda_station_25164.md
    ├── scripts/
    │   ├── run_data_pipeline.py
    │   ├── run_e2e_pipeline.py
    │   └── run_reports_generator_pipeline.py
    ├── src/
    │   └── conaigua/
    │       ├── core/
    │       │   └── contracts/
    │       │       ├── __init__.py
    │       │       ├── errors.py
    │       │       ├── events.py
    │       │       ├── messages.py
    │       │       └── schemas.py
    │       ├── data_pipeline/
    │       │   ├── dataset_cleaner.py
    │       │   ├── parser.py
    │       │   ├── pipeline_runner.py
    │       │   └── quality_report.py
    │       ├── eda_agent/
    │       │   ├── config/
    │       │   └── tools/
    │       ├── eda_engine/
    │       │   ├── correlation.py
    │       │   ├── data_loader.py
    │       │   ├── outliers.py
    │       │   ├── regression.py
    │       │   ├── run_eda_pipeline.py
    │       │   ├── seasonality.py
    │       │   └── stats.py
    │       ├── eda_reports_generator/
    │       │   ├── html_generator.py
    │       │   └── markdown_generator.py
    │       ├── orchestration/
    │       │   └── e2e_runner.py
    │       └── utils/
    │           ├── graph.py
    │           └── logger.py
    ├── tests/
    │   ├── integration/
    │   ├── conftest.py
    │   ├── test_agent_setup.py
    │   ├── test_cleaner.py
    │   ├── test_contract_integration.py
    │   ├── test_contracts.py
    │   ├── test_e2e_pipeline.py
    │   ├── test_llm_wrapper.py
    │   ├── test_parser.py
    │   ├── test_pipeline_integration.py
    │   ├── test_prompt.py
    │   ├── test_quality.py
    │   └── test_tools.py
    ├── .env.example
    ├── langgraph.json
    ├── pyproject.toml
    ├── README.md
    ├── README.en.md
    └── uv.lock
```
---

## Tests

```bash
pytest tests/test_us_3_3.py scripts\eda_agent\config\logger.py -v           
```
---

## Generate all reports in advance

If you want to pre-generate the reports for all stations before using the agent:

```bash
python -m scripts.run_reports_generator_pipeline
```

The reports will be placed in `reports/eda/html/` and `reports/eda/markdown/`. The agent will reuse them automatically without regenerating them.

---

## Traceability logs

The agent automatically logs every interaction in `logs/agent.log`:

```json
{"timestamp": "2026-03-22T08:29:27", "evento": "agent_start", "modelo": "razonamiento", "n_tools": 7}
{"timestamp": "2026-03-22T08:30:15", "evento": "interaction", "user_input": "Dame el promedio de precip de 25001", "response": "El promedio de precipitación...", "tools_used": []}
{"timestamp": "2026-03-22T08:31:05", "evento": "error", "user_input": "...", "error": "..."}
```

---

## Main dependencies

| Package | Use |
|---------|-----|
| `langchain` + `langgraph` | Agent framework and checkpointing with memory |
| `langchain-groq` | Integration with Groq (default provider) |
| `pandas` + `pyarrow` | Dataset processing |
| `scipy` + `scikit-learn` | Statistical correlations and regressions |
| `ydata-profiling` | Automatic HTML reports |
| `rich` | Markdown rendering in the terminal |
| `python-dotenv` | Environment variables |
| `pytest` | Automated tests |

---

## Notes

- The agent **only answers questions** related to hydrometeorological analysis for the ConAIgua project. Any out-of-scope request will be politely declined.
- Reports are generated automatically the first time they are requested and are reused for subsequent requests.
- The agent's memory uses LangGraph's `InMemorySaver` — conversation context is kept during the session but resets when it is closed.
- If you hit Groq's daily token limit, wait a few minutes or switch to the `llama-3.1-8b-instant` model in `agent_setup.py` for higher speed with lower consumption.
