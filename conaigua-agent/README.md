# ConAIgua — Agente EDA Hidrometeorológico

Agente conversacional especializado en análisis de datos hidrometeorológicos de estaciones CONAGUA en Sinaloa, México. Permite consultar estadísticas, correlaciones, regresiones y generar reportes mediante lenguaje natural desde la terminal.

---
<div align="center">

[English Version](README.en.md)

</div>

## Requisitos previos

- **Python 3.12** — [descargar aquí](https://www.python.org/downloads/)
- **uv** — gestor de paquetes (ver instalación abajo)
- **API Key** del proveedor LLM que vayas a usar (ver sección de proveedores)

### Instalar uv

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux / Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Con pip (alternativa universal):**
```bash
pip install uv
```

> Si prefieres no usar `uv`, puedes usar `pip` directamente.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Chris6264/ConAIgua.git
cd EdaAgent
```

### 2. Crear el entorno virtual con Python 3.12

```bash
uv venv --python 3.12 .venv
```

Sin `uv`:
```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

```bash
# Windows
.venv\Scripts\Activate.ps1

# Linux / Mac
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
uv pip install -e .
```

Sin `uv`:
```bash
pip install -e .
```

### 5. Configurar variables de entorno

Copia el archivo de ejemplo:

```bash
# Windows
copy .env.example .env

# Linux / Mac
cp .env.example .env
```
Copia el archivo de configuración:

```bash
# Windows
cd config
copy config.example.yaml config.yaml

# Linux / Mac
cd config
cp config.example.yaml config.yaml
```

Abre `.env` y configura tu proveedor y API key:

```dotenv
# Proveedor LLM — opciones: groq, openai, anthropic, google
LLM_PROVIDER="groq"

# Agrega SOLO la key del proveedor que vayas a usar
GROQ_API_KEY="tu_api_key_aqui"
OPENAI_API_KEY="tu_api_key_aqui"
ANTHROPIC_API_KEY="tu_api_key_aqui"
GOOGLE_API_KEY="tu_api_key_aqui"
```

Despues en el directorio config abre el archivo`config.yaml` y configura tu proveedor y API key:

```dotenv
llm:
  provider: groq #Coloca tu proveedor
  model: llama-3.3-70b-versatile #Coloca tu modelo
  api_key_env: "" #Coloca tu API key en forma de variable de entorno.
  temperature: 0
  max_tokens: 1024
```

### 6. Preparar el dataset

Los archivos `.txt` de las estaciones deben estar en `data/raw/`. Una vez ahí, genera el dataset procesado con el pipeline:

```bash
python -m scripts.run_data_pipeline
```

Esto creará `data/processed/conAIgua_dataframe.parquet`.

> Si ya tienes el archivo `.parquet`, puedes omitir este paso.

---

## Ejecución
Una vez generado el archivo procesado, el agente puede ejecutarse mediante LangGraph utilizando el siguiente comando:

```bash
PYTHONPATH="$PWD/src" uv run langgraph dev
```
Adicionalmente, para visualizar los reportes EDA generados en formato HTML, se puede levantar un servidor local desde la carpeta de reportes mediante los siguientes comando:

```bash
cd reports/eda 
python -m http.server 8088
```

Presiona `Ctrl + C` para terminar la sesión.

---

## Proveedores LLM

| Proveedor | `LLM_PROVIDER` | Obtener API Key | Tier gratuito |
|-----------|----------------|-----------------|---------------|
| **Groq** (recomendado) | `groq` | https://console.groq.com | Sí |
| OpenAI | `openai` | https://platform.openai.com/api-keys | No |
| Anthropic (Claude) | `anthropic` | https://console.anthropic.com | No |
| Google Gemini | `google` | https://aistudio.google.com/app/apikey | Sí |

El modelo por defecto es `qwen/qwen3-32b` en Groq. Puedes cambiarlo en `scripts/eda_agent/config/llm_wrapper.py` y ajustar el nivel (`rapido`, `balanceado`, `razonamiento`) y temperatura en `scripts/eda_agent/config/agent_setup.py`.

---

## Capacidades del agente

| Capacidad | Descripción |
|-----------|-------------|
| Estadísticas EDA | Media, mediana, min, max, std, outliers y estacionalidad |
| Correlaciones | Pearson y Spearman con p-value y significancia estadística |
| Regresiones | Lineal simple y múltiple con R², RMSE, IC 95% y diagnóstico |
| Tendencias | Análisis de tendencia anual en rangos de años |
| Reportes | HTML (ydata-profiling) y Markdown por estación |
| Estaciones | Listado de todas las estaciones disponibles |

### Variables disponibles

| Variable | Descripción | Unidad |
|----------|-------------|--------|
| `precip` | Precipitación | mm |
| `evap` | Evaporación | mm |
| `tmax` | Temperatura máxima | °C |
| `tmin` | Temperatura mínima | °C |
| `mes` | Mes del año | 1–12 |
| `anio` | Año del registro | — |

---

## Ejemplos de uso

```
¿Cuáles son las estaciones disponibles?
Dame el promedio de precipitación de la estación 25001
Dame el promedio de precipitación de la estación 25001 del año 1978
¿Cuál fue la correlación entre precipitación y temperatura máxima en la estación 25001?
Calcula la regresión lineal de precipitación contra mes en la estación 25001
Haz una regresión múltiple de precipitación contra mes y año en la estación 25001
¿Cuál es la tendencia de precipitación en la estación 25001 entre 1970 y 1980?
Generame un reporte de la estación 25001
Generame un reporte de la estación 25001 en html
```

---

## Estructura del proyecto

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

## Test

```bash
pytest tests/test_us_3_3.py scripts\eda_agent\config\logger.py -v           
```
---

## Generar todos los reportes por adelantado

Si deseas pre-generar los reportes de todas las estaciones antes de usar el agente:

```bash
python -m scripts.run_reports_generator_pipeline
```

Los reportes quedarán en `reports/eda/html/` y `reports/eda/markdown/`. El agente los reutilizará automáticamente sin regenerarlos.

---

## Logs de trazabilidad

El agente registra cada interacción automáticamente en `logs/agent.log`:

```json
{"timestamp": "2026-03-22T08:29:27", "evento": "agent_start", "modelo": "razonamiento", "n_tools": 7}
{"timestamp": "2026-03-22T08:30:15", "evento": "interaction", "user_input": "Dame el promedio de precip de 25001", "response": "El promedio de precipitación...", "tools_used": []}
{"timestamp": "2026-03-22T08:31:05", "evento": "error", "user_input": "...", "error": "..."}
```

---

## Dependencias principales

| Paquete | Uso |
|---------|-----|
| `langchain` + `langgraph` | Framework del agente y checkpointing con memoria |
| `langchain-groq` | Integración con Groq (proveedor por defecto) |
| `pandas` + `pyarrow` | Procesamiento del dataset |
| `scipy` + `scikit-learn` | Correlaciones y regresiones estadísticas |
| `ydata-profiling` | Reportes HTML automáticos |
| `rich` | Renderizado Markdown en terminal |
| `python-dotenv` | Variables de entorno |
| `pytest` | Tests automatizados |

---

## Notas

- El agente **solo responde preguntas** relacionadas con análisis hidrometeorológico del proyecto ConAIgua. Cualquier solicitud fuera de contexto será rechazada educadamente.
- Los reportes se generan automáticamente la primera vez que se solicitan y se reutilizan en solicitudes posteriores.
- La memoria del agente usa `InMemorySaver` de LangGraph — el contexto de la conversación se mantiene durante la sesión pero se reinicia al cerrar.
- Si llegas al límite de tokens diarios de Groq, espera unos minutos o cambia al modelo `llama-3.1-8b-instant` en `agent_setup.py` para mayor velocidad con menor consumo.
