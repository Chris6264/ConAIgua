<div align="center">

# ConAIgua — Hydrometeorological Query System with LLM

![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)
![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

[Versión en Español](README.md)

</div>

Conversational agent for querying CONAGUA's (Mexico's National Water Commission) historical hydrometeorological data through natural language, built on top of LangGraph and an LLM served by Groq (default provider, can be swapped for another), with tools, prompts, and rules purpose-built for the climatological domain.

---

## Overview

**ConAIgua** lets you query statistics, correlations, regressions, and trends over CONAGUA's historical dataset without writing code or SQL. It is not a model trained from scratch: it uses a base model served by Groq (e.g. `llama-3.3-70b-versatile`), to which the backend adds **custom tools, prompts, business rules, and generation parameters** specific to hydrometeorological analysis.

### What problem does it solve?

Historical hydrometeorological data is usually stored in hard-to-access formats (plain `.txt` files per station, with metadata and daily series mixed together). ConAIgua allows:

- **Natural-language queries**: "What was the maximum temperature at the ALTO DE CULIACANCITO station in January 1978?"
- **Statistical analysis**: mean, median, outliers, correlations (Pearson/Spearman), regressions (simple/multiple), annual trends
- **Automatic reports**: generation of EDA reports in HTML and Markdown per station
- **Specialized domain**: the agent understands the structure of CONAGUA stations, their keys, states, and municipalities

---

## High-level architecture

Current state: the web interface talks to a backend built on LangGraph, which in turn calls the LLM hosted on Groq. No external databases are in use yet.

```text
┌─────────────┐  HTTPS/WSS  ┌──────────────┐
│  Frontend   │ ◄──────────►│ API Backend  │
│  (React +   │             │ (LangGraph)  │
│  Next.js)   │             └───────┬──────┘
└─────────────┘                     │
                                    │
                                    │  HTTPS/WSS
                                    ▼
                        ┌──────────────────────────┐
                        │   LLM (Groq)             │
                        │   Configured for         │
                        │   ConAIgua: tools,       │
                        │   prompts, and custom    │
                        │   rules over CONAGUA     │
                        │   data                   │
                        └──────────────────────────┘
```

- **Frontend**: React + Next.js. Sends the user's queries and displays the agent's responses.
- **API Backend (LangGraph)**: orchestrates the data pipeline, the EDA engine, and the conversation; exposes the agent to the frontend via HTTPS/WSS.
- **LLM (Groq)**: base model, not trained from scratch. What makes ConAIgua specific is the set of tools, prompts, and rules the backend injects into every call.

> **Roadmap (not implemented yet):** user/session persistence (PostgreSQL), chat history (MongoDB), and semantic search (Qdrant). These will be documented here once they're actually integrated, not before.

---

## Real CONAGUA dataset format

The dataset comes from the **National Climatological Database** (CNA-SMN-CG-GMC-SMAA-CLIMATOLOGIA), with data supplied by CONAGUA's Regional Offices. Each station file has the following format:

```text
ESTACION  : 25164
NOMBRE    : ALTO DE CULIACANCITO
ESTADO    : SINALOA
MUNICIPIO : CULIACAN
SITUACION : SUSPENDIDA
ORGANISMO : CONAGUA-DGE
CVE-OMM   : Nulo
LATITUD   : 024.807
LONGITUD  : -107.555
ALTITUD   : 24 msnm

EMISION   : 06/04/2020

           PRECIP  EVAP   TMAX   TMIN
  FECHA     (MM)   (MM)   (C)    (C)
01/01/1978  0     Nulo    24     12
02/01/1978  0     Nulo    26     16
03/01/1978  0     Nulo    30     11
...
```

### Station metadata

| Field | Description | Example |
|---|---|---|
| `ESTACION` | Unique station key | `25164` |
| `NOMBRE` | Station name | `ALTO DE CULIACANCITO` |
| `ESTADO` | Mexican state | `SINALOA` |
| `MUNICIPIO` | Station municipality | `CULIACAN` |
| `SITUACIÓN` | Operational status | `SUSPENDIDA` / `ACTIVA` |
| `ORGANISMO` | Responsible agency | `CONAGUA-DGE` |
| `CVE-OMM` | International WMO code | `Nulo` or numeric code |
| `LATITUD` / `LONGITUD` | Geographic coordinates | `024.807°` / `-107.555°` |
| `ALTITUD` | Meters above sea level | `24 msnm` |
| `EMISION` | Report issue date | `06/04/2020` |

### Daily records

| Field | Description | Unit |
|---|---|---|
| `FECHA` | Observation date | `DD/MM/YYYY` |
| `PRECIP` | Accumulated precipitation | mm |
| `EVAP` | Evaporation | mm |
| `TMAX` | Daily maximum temperature | °C |
| `TMIN` | Daily minimum temperature | °C |

---

## Data pipeline

```text
┌────────────┐   ┌──────────────┐   ┌──────────────────┐
│ Plain TXT  │ → │  Pandas      │ → │  Parquet Store   │
│ CONAGUA    │   │  Transform   │   │  (final dataset) │
└────────────┘   └──────────────┘   └──────────────────┘
```

The pipeline (`run_data_pipeline`) parses CONAGUA's proprietary format, treats the `Nulo` literal as a missing value, cleans the dataset, and converts it into `data/processed/conAIgua_dataframe.parquet`, which is what the agent consumes.

---

## Agent capabilities

| Capability | Description |
|---|---|
| EDA statistics | Mean, median, min, max, std, outliers, and seasonality |
| Correlations | Pearson and Spearman with p-value and statistical significance |
| Regressions | Simple and multiple linear regression with R², RMSE, 95% CI, and diagnostics |
| Trends | Annual trend analysis over year ranges |
| Reports | HTML (ydata-profiling) and Markdown per station |
| Stations | Listing of all available stations |

---

## Tech stack

| Area | Technology |
|---|---|
| Frontend | React 18, Next.js 14, pnpm, Docker |
| Backend / Agent | Python 3.12, LangChain, LangGraph |
| Data | pandas, pyarrow (Parquet) |
| Statistics | scipy, scikit-learn |
| Reports | ydata-profiling |
| Supported LLM providers | Groq (default), OpenAI, Anthropic, Google Gemini |

---

## Getting started

The system runs in two parts:

1. **Agent** — installation, data pipeline, and running with LangGraph: [`conaigua-agent/README.en.md`](conaigua-agent/README.en.md)
2. **Web interface** — dependency installation and running with Docker: [`conaigua-chat-ui/README.en.md`](conaigua-chat-ui/README.en.md)
---

## Screenshots

**General view of the interface**

<img width="1850" height="657" alt="General view of the interface" src="https://github.com/user-attachments/assets/53e75300-5335-4ef6-b0b6-09c0947aaa9c" />

**Chatting with the agent**

<img width="1852" height="926" alt="Chat con el agente" src="https://github.com/user-attachments/assets/9f72bbd2-8a70-4b27-9bc9-59ce24a056ae" />

<img width="869" height="358" alt="image" src="https://github.com/user-attachments/assets/e12073a7-64ea-4288-a99f-fa231fbffe00" />

<img width="869" height="358" alt="image" src="https://github.com/user-attachments/assets/e1e97fdd-34b0-4ad9-a53c-1bfd93495a10" />

**Asking the agent for an HTML report**

<img width="1416" height="653" alt="Reporte EDA en HTML" src="https://github.com/user-attachments/assets/dab65656-a471-4fe7-a939-cf0e90af32c5" />

<img width="869" height="358" alt="image" src="https://github.com/user-attachments/assets/fdd941e2-7e00-45a1-b59b-3063e071d3da" />

**EDA report in HTML**

<img width="1849" height="912" alt="EDA report in HTML" src="https://github.com/user-attachments/assets/115de2cd-9727-4476-a204-9a37934307ab" />

---

## License

Copyright © 2026 Chris6264

This project is distributed under the [Apache 2.0 License](LICENSE).
