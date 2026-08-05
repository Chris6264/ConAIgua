# ConAIgua — Hydrometeorological EDA Agent

Conversational agent specialized in hydrometeorological data analysis from CONAGUA stations in Sinaloa, Mexico. Allows querying statistics, correlations, regressions, and generating reports through natural language from the terminal.

---
<div align="center">

[Versión en Español](README.md)

</div>

## Prerequisites

- **Python 3.12** — [download here](https://www.python.org/downloads/)
- **uv** — package manager (see installation below)
- **API Key** from the LLM provider you plan to use (see providers section)

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

Open `.env` and configure your provider and API key:

```dotenv
# LLM Provider — options: groq, openai, anthropic, google
LLM_PROVIDER="groq"

# Add ONLY the key for the provider you are going to use
GROQ_API_KEY="your_api_key_here"
OPENAI_API_KEY="your_api_key_here"
ANTHROPIC_API_KEY="your_api_key_here"
GOOGLE_API_KEY="your_api_key_here"
```

### 6. Prepare the dataset

The station `.txt` files must be placed in `data/raw/`. Once there, generate the processed dataset:

```bash
python -m scripts.dataset_generator.dataset_generator
```

This will create `data/processed/conAIgua_dataframe.parquet`.

> If you already have the `.parquet` file, you can skip this step.

---
## Execution

Once the processed file has been generated, the agent can be run with LangGraph using the following command:

```bash
uv run langgraph dev
```

Additionally, to view the generated EDA reports in HTML format, start a local server from the reports directory:

```bash
cd reports/eda
python -m http.server 8080
```

Then open the following URL in your browser:

```text
http://localhost:8080
```

Press `Ctrl + C` to stop the server.
---

## LLM Providers

| Provider | `LLM_PROVIDER` | Get API Key | Free Tier |
|----------|----------------|-------------|-----------|
| **Groq** (recommended) | `groq` | https://console.groq.com | Yes |
| OpenAI | `openai` | https://platform.openai.com/api-keys | No |
| Anthropic (Claude) | `anthropic` | https://console.anthropic.com | No |
| Google Gemini | `google` | https://aistudio.google.com/app/apikey | Yes |

The default model is `qwen/qwen3-32b` on Groq. You can change it in `scripts/eda_agent/config/llm_wrapper.py` and adjust the level (`rapido`, `balanceado`, `razonamiento`) and temperature in `scripts/eda_agent/config/agent_setup.py`.

---

## Agent Capabilities

| Capability | Description |
|------------|-------------|
| EDA Statistics | Mean, median, min, max, std, outliers and seasonality |
| Correlations | Pearson and Spearman with p-value and statistical significance |
| Regressions | Simple and multiple linear with R², RMSE, 95% CI and diagnostics |
| Trends | Annual trend analysis over year ranges |
| Reports | HTML (ydata-profiling) and Markdown per station |
| Stations | List of all available stations |

### Available Variables

| Variable | Description | Unit |
|----------|-------------|------|
| `precip` | Precipitation | mm |
| `evap` | Evaporation | mm |
| `tmax` | Maximum temperature | °C |
| `tmin` | Minimum temperature | °C |
| `mes` | Month of the year | 1–12 |
| `anio` | Year of the record | — |

---

## Usage Examples

```
Which stations are available?
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

## Project Structure

```
EdaAgent/
├── src/
│ └── conaigua/
│ ├── init.py
│ └── main.py # Entry Point CLI
│
├── .env.example                         # Environment variables template
├── pyproject.toml                       # Project dependencies
│
├── data/
│   ├── raw/                             # CONAGUA station .txt files
│   │   ├── 25001.txt
│   │   └── ...
│   └── processed/
│       └── conAIgua_dataframe.parquet   # Processed dataset
│
├── logs/
│   └── agent.log                        # Interaction traceability
│
├── notebooks/
│   ├── US_3_2_modelado.ipynb            # Regression and correlation examples
│   └── ...
│
├── reports/
│   └── eda/
│       ├── html/                        # HTML reports per station
│       └── markdown/                    # Markdown reports per station
│
├── scripts/
│   ├── dataframe_generator/
│   │   ├── dataset_generator.py         # Generates parquet from .txt files
│   │   ├── dataframe_cleaner.py         # Dataframe cleaning
│   │   └── parser.py                    # CONAGUA file parser
│   │
│   ├── eda_agent/
│   │   ├── config/
│   │   │   ├── agent_setup.py           # Agent and tools configuration
│   │   │   ├── llm_wrapper.py           # Multi-provider LLM wrapper
│   │   │   └── logger.py                # Traceability logging system
│   │   └── tools/
│   │       ├── eda_tool.py              # Full EDA analysis
│   │       ├── stats_tool.py            # Basic statistics
│   │       ├── full_correlation_tool.py # Pearson/Spearman correlation
│   │       ├── regression_tool.py       # Simple and multiple linear regression
│   │       ├── trend_tool.py            # Annual trend
│   │       ├── report_tool.py           # Report generation
│   │       ├── stations_tool.py         # Station listing
│   │       └── filter_tool.py           # Data filtering
│   │
│   ├── eda_engine/
│   │   ├── data_loader.py               # Dataset loading
│   │   ├── eda_pipeline.py              # EDA pipeline
│   │   ├── correlation.py               # Pearson/Spearman correlations
│   │   ├── regression.py                # Linear regressions
│   │   ├── stats.py                     # Descriptive statistics
│   │   ├── outliers.py                  # IQR outlier detection
│   │   └── seasonality.py               # Seasonality patterns
│   │
│   └── eda_reports_generator/
│       ├── html_generator.py            # HTML report generator
│       ├── markdown_generator.py        # Markdown report generator
│       └── reports_generator.py         # Generates reports for all stations
│
└── tests/
    └── test_us_3_3.py                   # LLM wrapper and agent tests
```

---

## Tests

```bash
pytest tests/test_us_3_3.py scripts\eda_agent\config\logger.py -v
```

---

## Pre-generate All Reports

If you want to pre-generate reports for all stations before using the agent:

```bash
python -m scripts.eda_reports_generator.reports_generator
```

Reports will be saved in `reports/eda/html/` and `reports/eda/markdown/`. The agent will reuse them automatically without regenerating.

---

## Traceability Logs

The agent automatically records each interaction in `logs/agent.log`:

```json
{"timestamp": "2026-03-22T08:29:27", "evento": "agent_start", "modelo": "razonamiento", "n_tools": 7}
{"timestamp": "2026-03-22T08:30:15", "evento": "interaction", "user_input": "Give me the average precip for 25001", "response": "The average precipitation...", "tools_used": []}
{"timestamp": "2026-03-22T08:31:05", "evento": "error", "user_input": "...", "error": "..."}
```

---

## Main Dependencies

| Package | Use |
|---------|-----|
| `langchain` + `langgraph` | Agent framework and memory checkpointing |
| `langchain-groq` | Groq integration (default provider) |
| `pandas` + `pyarrow` | Dataset processing |
| `scipy` + `scikit-learn` | Statistical correlations and regressions |
| `ydata-profiling` | Automatic HTML reports |
| `rich` | Markdown rendering in terminal |
| `python-dotenv` | Environment variables |
| `pytest` | Automated tests |

---

## Notes

- The agent **only answers questions** related to hydrometeorological analysis of the ConAIgua project. Any out-of-context request will be politely rejected.
- Reports are generated automatically the first time they are requested and reused in subsequent requests.
- The agent's memory uses `InMemorySaver` from LangGraph — conversation context is maintained during the session but resets on close.
- If you reach Groq's daily token limit, wait a few minutes or switch to the `llama-3.1-8b-instant` model in `agent_setup.py` for faster responses with lower consumption.
