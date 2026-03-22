<div align="center">

# ConAIgua - Hydrometeorological Data Query System with LLM

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Rust](https://img.shields.io/badge/Rust-1.75+-orange.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

[Versión en Español](README.md)

</div>

Intelligent chatbot for querying historical hydrometeorological data from CONAGUA (Mexico's National Water Commission) using natural language processing, powered by an **LLM trained from scratch** on exclusive CONAGUA data.

## Overview

**ConAIgua** is a hydrometeorological data query system that uses a **custom Large Language Model (LLM)**, trained entirely from scratch on historical data from CONAGUA (Comisión Nacional del Agua de México), combined with **Retrieval-Augmented Generation (RAG)** to deliver precise and contextual answers in natural language.

> **Important**: The language model used in ConAIgua is **not an external or pre-existing LLM** (it is not GPT, Claude, LLaMA, or any third-party model). It is a model **designed, trained, and optimized from scratch** using exclusively the CONAGUA dataset, hydrometeorological data processing pipelines, and custom Transformer architectures. This ensures the model has deep, specialized knowledge of the Mexican climatological domain.

### What problem does it solve?

Historical hydrometeorological data is often stored in inaccessible formats (plain TXT files, CSVs, complex databases). This chatbot enables:

- **Natural language queries**: "What was the maximum temperature in Culiacán in January 1978?"
- **Climatological data analysis**: Precipitation, evaporation, daily maximum and minimum temperature
- **Semantic search**: RAG over the CONAGUA dataset for precise, contextual responses
- **Real-time responses**: Interactive web interface with response streaming
- **Specialized domain**: The LLM natively understands CONAGUA station structures, identifiers, Mexican states and municipalities

### High-Level Architecture

```
┌─────────────┐  HTTPS/WSS  ┌──────────────┐
│  Frontend   │ ◄──────────►│ API Backend  │
│  (React +   │             │    (Rust)    │
│  Next.js)   │             └───────┬──────┘
└─────────────┘                     │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
    ┌───────────────┐     ┌─────────────┐     ┌─────────────┐
    │  PostgreSQL   │     │   MongoDB   │     │   Qdrant    │
    │  (Users/      │     │   (Chat     │     │   (Vector   │
    │  Sessions)    │     │   History)  │     │   DB)       │
    └───────────────┘     └─────────────┘     └─────────────┘
                                │
                                ▼
                   ┌────────────────────────┐
                   │  ConAIgua LLM (Custom) │
                   │  Trained from scratch  │
                   │  on CONAGUA data       │
                   └────────────────────────┘
```

---

## The ConAIgua LLM: Custom Model Trained from Scratch

### Why a custom LLM?

Unlike systems that rely on generic models (OpenAI, Anthropic, Meta, etc.), ConAIgua builds its own language model trained exclusively on Mexican hydrometeorological data. This enables:

- **Full domain specialization**: The model natively understands CONAGUA stations, their keys, responsible agencies, Mexican states and municipalities
- **Data privacy and sovereignty**: No information is sent to external services
- **Complete model control**: Fine-tuning, versioning, and deployment fully under our control
- **No third-party dependency**: No API costs and no risk of service discontinuation

### Real CONAGUA Dataset Format

The dataset comes from the **National Climatological Database** (CNA-SMN-CG-GMC-SMAA-CLIMATOLOGIA), with data provided by CONAGUA's Regional Offices. Each station file has the following format:

```
ESTACION  : 25164
NOMBRE    : ALTO DE CULIACANCITO
ESTADO    : SINALOA
MUNICIPIO : CULIACAN
SITUACIÓN : SUSPENDIDA
ORGANISMO : CONAGUA-DGE
CVE-OMM   : Nulo
LATITUD   : 024.807°
LONGITUD  : -107.555°
ALTITUD   : 24 msnm

EMISION   : 06/04/2020

           PRECIP  EVAP   TMAX   TMIN
  FECHA     (MM)   (MM)   (°C)   (°C)
01/01/1978  0     Nulo    24     12
02/01/1978  0     Nulo    26     16
03/01/1978  0     Nulo    30     11
...
```

### CONAGUA Dataset Structure

**Station Metadata:**

| Field | Description | Example |
|---|---|---|
| `ESTACION` | Unique station key | `25164` |
| `NOMBRE` | Station name | `ALTO DE CULIACANCITO` |
| `ESTADO` | Mexican state | `SINALOA` |
| `MUNICIPIO` | Station municipality | `CULIACAN` |
| `SITUACIÓN` | Operational status | `SUSPENDIDA` / `ACTIVA` |
| `ORGANISMO` | Responsible agency | `CONAGUA-DGE` |
| `CVE-OMM` | International WMO key | `Nulo` or numeric code |
| `LATITUD` | Geographic coordinate | `024.807°` |
| `LONGITUD` | Geographic coordinate | `-107.555°` |
| `ALTITUD` | Meters above sea level | `24 msnm` |
| `EMISION` | Report emission date | `06/04/2020` |

**Daily Records:**

| Field | Description | Unit |
|---|---|---|
| `FECHA` | Observation date | `DD/MM/YYYY` | 
| `PRECIP` | Accumulated precipitation | mm | 
| `EVAP` | Evaporation | mm | 
| `TMAX` | Daily maximum temperature | °C | 
| `TMIN` | Daily minimum temperature | °C |

### LLM Training Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                  ConAIgua LLM TRAINING PIPELINE                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DATA INGESTION                                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  CONAGUA Dataset (plain TXT files per station)          │    │
│  │  • Metadata: key, name, state, municipality,            │    │
│  │    status, agency, coordinates, altitude                │    │
│  │  • Daily series: PRECIP, EVAP, TMAX, TMIN               │    │
│  │  • Historical coverage from 1920s to 2020               │    │
│  │  • Thousands of stations across all of Mexico           │    │
│  └──────────────────────────┬──────────────────────────────┘    │ 
│                             │                                   │
│  2. PREPROCESSING                                               │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Cleaning & Normalization Pipeline (Polars/Pandas)      │    │
│  │  • Parsing of CONAGUA's proprietary TXT format          │    │
│  │  • Handling of literal "Nulo" string → NaN              │    │ 
│  │  • Temporal interpolation of missing values             │    │
│  │  • Climatological outlier detection and correction      │    │
│  │  • Coordinate and altitude normalization                │    │
│  │  • Conversion to structured tabular format              │    │ 
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  3. CORPUS BUILDING                                             │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Training Corpus Generation                             │    │
│  │  • Synthetic (question, answer) pairs                   │    │
│  │    e.g. "TMAX at station 25164 on 09/01/1978?" → "31°C" │    │
│  │  • Monthly and annual summaries per station             │    │
│  │  • Enriched geographic context (state, municipality)    │    │
│  │  • CONAGUA and climatological terminology vocabulary    │    │
│  └──────────────────────────┬──────────────────────────────┘    │ 
│                             │                                   │
│  4. MODEL TRAINING                                              │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Transformer Architecture (from scratch)                │    │
│  │  • Pre-training: Causal Language Modeling (CLM)         │    │
│  │  • Supervised fine-tuning: climatological Q&A pairs     │    │
│  │  • Optional RLHF: human feedback on responses           │    │
│  │  • Framework: PyTorch + HuggingFace Trainer (internal)  │    │
│  └──────────────────────────┬──────────────────────────────┘    │ 
│                             │                                   │
│  5. EVALUATION & VALIDATION                                     │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Quality Metrics                                        │    │
│  │  • Perplexity on CONAGUA validation corpus              │    │
│  │  • BLEU / ROUGE on reference responses                  │    │ 
│  │  • Human evaluation of climatological accuracy          │    │
│  │  • Latency and throughput benchmarks                    │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  6. DEPLOYMENT                                                  │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Model Serving                                          │    │
│  │  • Export to ONNX or TorchScript                        │    │
│  │  • INT8/FP16 quantization for efficiency                │    │
│  │  • Serving via internal REST API (Rust ↔ Python bridge) │    │
│  │  • Model versioning with MLflow                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Pipelines

```
┌──────────────────────────────────────────────────────────────┐
│                        DATA PIPELINES                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Pipeline 1: ETL (Extract, Transform, Load)                  │
│  ┌────────────┐   ┌──────────────┐   ┌──────────────────┐    │
│  │ Plain TXT  │ → │  Polars      │ → │  PostgreSQL /    │    │
│  │ CONAGUA    │   │  Transform   │   │  Parquet Store   │    │
│  └────────────┘   └──────────────┘   └──────────────────┘    │
│                                                              │
│  Pipeline 2: Embedding for RAG                               │
│  ┌────────────┐   ┌──────────────┐   ┌──────────────────┐    │
│  │  Clean     │ → │  Tokenizer   │ → │  Qdrant Vector   │    │
│  │  data      │   │  + Encoder   │   │  DB (embeddings) │    │
│  └────────────┘   └──────────────┘   └──────────────────┘    │
│                                                              │
│  Pipeline 3: Continuous Training                             │
│  ┌────────────┐   ┌──────────────┐   ┌──────────────────┐    │
│  │  New       │ → │  Incremental │ → │  Model Registry  │    │  
│  │  data      │   │  fine-tuning │   │  (MLflow)        │    │
│  └────────────┘   └──────────────┘   └──────────────────┘    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Key Features

### Artificial Intelligence
- **Custom LLM (ConAIgua Model)**: Transformer model trained from scratch on CONAGUA data — no dependency on external APIs
- **RAG (Retrieval-Augmented Generation)**: Semantic search over the CONAGUA dataset to enrich responses with precise data
- **Vector Embeddings**: Qdrant for efficient climatological context retrieval
- **Response Streaming**: WebSocket for real-time responses
- **Continuous Training**: Pipeline for retraining with new CONAGUA data

### Frontend (React + Next.js)
- **Server-Side Rendering (SSR)**: Fast initial load and optimized SEO
- **Static Site Generation (SSG)**: Static pages for non-dynamic content
- **App Router**: Modern routing with nested layouts (Next.js 14+)
- **React Server Components**: Reduced client-side JS bundle
- **API Routes**: Backend-for-Frontend integrated in Next.js

### Climatological Data
- **CONAGUA Dataset**: National Climatological Database with daily records dating back to the 1920s
- **4 Climate Variables**: Precipitation (mm), Evaporation (mm), Maximum Temperature (°C), Minimum Temperature (°C)
- **Thousands of Stations**: Coverage across all of Mexico
- **Temporal Queries**: Date ranges, monthly/annual aggregations, trends, and anomalies

### Security
- **Microsegmentation**: Component isolation with Network Policies
- **Zero Trust Architecture**: Authentication and authorization at every layer
- **Encryption**: TLS 1.3 in transit, AES-256 at rest
- **JWT Authentication**: RS256 tokens with automatic rotation
- **WAF**: OWASP Top 10 protection
- **Auditing**: Full structured logging with SIEM integration

### Performance
- **Smart Cache**: Redis for sessions and frequent results
- **Async/Await**: Fully asynchronous backend in Rust
- **Connection Pooling**: Optimized database connections
- **Rate Limiting**: Abuse prevention
- **Model Quantization**: INT8/FP16 for efficient LLM inference

---

## System Architecture

### Hexagonal Architecture (Ports & Adapters)

The project follows **Hexagonal Architecture** principles (also known as Ports and Adapters), ensuring:

- **Separation of Concerns**: Business logic independent of frameworks
- **Testability**: Easy creation of unit and integration tests
- **Flexibility**: Technology changes without affecting core logic
- **Maintainability**: Organized and scalable codebase

```
┌─────────────────────────────────────────────────────────────┐
│                   HEXAGONAL ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ADAPTERS (Infrastructure)               │   │
│  │                                                      │   │
│  │   ┌─────────────┐          ┌─────────────┐           │   │
│  │   │  REST API   │          │  WebSocket  │           │   │
│  │   │   (Axum)    │          │   (Axum)    │           │   │
│  │   └──────┬──────┘          └──────┬──────┘           │   │
│  └─────────┼────────────────────────│───────────────────┘   │
│            │                        │                       │
│            │      PRIMARY PORTS (Input)                     │
│            ▼                        ▼                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    DOMAIN CORE                       │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │       Application Services (Use Cases)         │  │   │
│  │  │       • ChatOrchestrator                       │  │   │ 
│  │  │       • AuthenticationService                  │  │   │
│  │  │       • SessionManager                         │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │        Domain Logic (Business Rules)           │  │   │
│  │  │        • IntentParser                          │  │   │
│  │  │        • RAGService                            │  │   │ 
│  │  │        • ConAIguaLLMService (custom model)     │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │        Domain Entities (Models)                │  │   │
│  │  │        • User, Session, Message                │  │   │
│  │  │        • ChatContext, EmbeddingVector          │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └───────────────────────┬──────────────────────────────┘   │
│                          │                                  │
│            SECONDARY PORTS (Output)                         │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ADAPTERS (Infrastructure)               │   │
│  │                                                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐     │   │
│  │  │PostgreSQL│ │ MongoDB  │ │  Qdrant  │ │Redis │     │   │ 
│  │  │Repository│ │Repository│ │Repository│ │Cache │     │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────┘     │   │
│  │                                                      │   │
│  │  ┌──────────────────────┐  ┌────────────────────┐    │   │
│  │  │ ConAIgua LLM Client  │  │ CONAGUA DataFrame  │    │   │
│  │  │ (custom model,       │  │ (Polars/Pandas)    │    │   │
│  │  │  served locally)     │  │                    │    │   │
│  │  └──────────────────────┘  └────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Architecture Advantages

1. **Domain-Driven Design (DDD)**: Business logic is the core
2. **Dependency Inversion**: Dependencies point toward the domain
3. **Plug & Play**: Easy LLM versioning without affecting business logic
4. **Testing**: Simple port mocks for unit testing
5. **Clean Code**: Clear separation of responsibilities

### Microsegmentation & Security

The system implements **microsegmentation** following the **Zero Trust** model:

```
┌───────────────────────────────────────────────────────────┐
│  SEGMENT 1: Authentication                                │
│  • Auth Service, Session Manager                          │
│  • Access: PostgreSQL:5432, Redis:6379                    │
│  • Blocked: MongoDB, Qdrant, LLM Service, Internet        │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│  SEGMENT 2: Backend Services                              │
│  • Chat Orchestrator, RAG, ConAIgua LLM Service           │
│  • Access: MongoDB:27017, Qdrant:6333, LLM Service:8080   │
│  • Blocked: PostgreSQL (Auth only), Internet              │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│  SEGMENT 3: LLM Inference                                 │
│  • ConAIgua Model Server (PyTorch / ONNX Runtime)         │
│  • Access: Backend Services only                          │
│  • No Internet access, no database access                 │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│  SEGMENT 4: Data Layer                                    │
│  • PostgreSQL, MongoDB, Qdrant, Redis                     │
│  • Internal firewall with IP whitelisting                 │
│  • Access: Authorized services per port only              │
└───────────────────────────────────────────────────────────┘
```

**Implementation**: Kubernetes Network Policies or AWS Security Groups

### C4 Diagrams

The project includes full documentation following the **C4 model** (Context, Containers, Components, Code):

- **Level 1 - Context**: System overview and actors
- **Level 2 - Containers**: Applications and databases
- **Level 3 - Components**: Internal detail of the API Backend and LLM pipeline
- **Data View**: Storage structure and CONAGUA dataset
- **Security View**: Security layers and microsegmentation

See the `/docs/architecture/` folder for complete diagrams.

### Databases

| Technology | Usage | Type |
|---|---|---|
| **PostgreSQL** | Users, sessions, audit logs | Relational |
| **MongoDB** | Conversation history | Document |
| **Qdrant** | Vector embeddings (RAG) | Vector |
| **Redis** | Cache, rate limiting | In-memory |

### Full Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| **Frontend** | React 18 + Next.js 14 | App Router, SSR, RSC |
| **Backend API** | Rust (Axum) | Async, high performance |
| **LLM** | PyTorch + custom Transformer | Trained from scratch on CONAGUA |
| **RAG** | Qdrant + custom embeddings | ConAIgua model vectors |
| **Data Pipeline** | Polars / Pandas | CONAGUA ETL (TXT → tabular) |
| **Model Serving** | ONNX Runtime / TorchServe | Optimized local inference |
| **Relational DB** | PostgreSQL | Users and sessions |
| **Document DB** | MongoDB | Chat history |
| **Cache** | Redis | Sessions and rate limiting |
| **Infrastructure** | Docker + Kubernetes | Containerization and orchestration |
| **Reverse Proxy** | Nginx | Load balancing and TLS |
| **MLOps** | MLflow | LLM model versioning |

### Infrastructure

- **Docker** + **Docker Compose**: Containerization
- **Kubernetes** (optional): Orchestration and Network Policies
- **Nginx**: Reverse proxy and load balancing
- **Let's Encrypt**: SSL/TLS certificates
- **MLflow**: ConAIgua LLM model registry and versioning

---

## Security

### Implemented Controls

#### Network Layer
- Perimeter firewall with IPS/IDS
- WAF (Web Application Firewall)
- DDoS protection
- Mandatory TLS 1.3
- Optional geo-blocking

#### Authentication & Authorization
- JWT with RS256 (asymmetric)
- Argon2 for passwords (cost factor 12)
- Refresh token rotation
- RBAC (Role-Based Access Control)
- Configurable session timeout
- Optional MFA (TOTP)

#### Application Protection
- Input sanitization
- SQL/NoSQL injection prevention
- XSS protection (CSP headers)
- CSRF tokens
- Per-user/IP rate limiting
- Request size limits

#### Data
- Encryption at rest (AES-256)
- Encryption in transit (TLS)
- Secrets management (Vault / AWS Secrets)
- Backup encryption
- Data masking in logs

#### Microsegmentation
- Network Policies (K8s) or Security Groups (AWS)
- Per-segment isolation (including dedicated LLM segment)
- Default Deny
- Least privilege access

### Auditing & Compliance
- Structured logging (JSON)
- SIEM integration
- Security alerts
- Compliance: GDPR, SOC2

---

## License

Copyright © 2026 Chris6264

Licensed under the Apache License, Version 2.0.
