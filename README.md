# ConAIgua - Sistema de Consultas Meteorológicas con LLM

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![Rust](https://img.shields.io/badge/Rust-1.75+-orange.svg) ![React](https://img.shields.io/badge/React-18+-61DAFB.svg) ![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg) ![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg) ![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow.svg)

Chatbot inteligente que permite consultar información meteorológica histórica de CONAGUA mediante procesamiento de lenguaje natural, impulsado por un **LLM entrenado desde cero** con datos exclusivos de CONAGUA.

## Descripción General

**ConAIgua** es un sistema de consulta de información meteorológica que utiliza un **Large Language Model (LLM) propio**, entrenado íntegramente desde cero con datos históricos de CONAGUA (Comisión Nacional del Agua de México), combinado con **Retrieval-Augmented Generation (RAG)** para proporcionar respuestas precisas y contextuales en lenguaje natural.

> **Importante**: El modelo de lenguaje utilizado en ConAIgua **no es un LLM externo ni preexistente** (no es GPT, Claude, LLaMA, ni ningún modelo de terceros). Es un modelo **diseñado, entrenado y optimizado desde cero** utilizando exclusivamente el dataset de CONAGUA, pipelines de procesamiento de datos meteorológicos y arquitecturas Transformer propias. Esto garantiza que el modelo tenga conocimiento profundo y especializado del dominio meteorológico mexicano.

### ¿Qué problema resuelve?

Los datos meteorológicos históricos suelen estar en formatos poco accesibles (CSVs, bases de datos complejas). Este chatbot permite:

- **Consultas en lenguaje natural**: "¿Cuál fue la temperatura en Culiacán la semana pasada?"
- **Análisis de datos meteorológicos**: Temperaturas, precipitación, humedad, viento, presión atmosférica
- **Búsqueda semántica**: RAG sobre dataset CONAGUA para respuestas contextuales precisas
- **Respuestas en tiempo real**: Interfaz web interactiva con streaming de respuestas
- **Dominio especializado**: El LLM entiende terminología, estaciones y patrones climáticos mexicanos de forma nativa

### Arquitectura de Alto Nivel

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
                   │  ConAIgua LLM (Propio) │
                   │  Entrenado desde cero  │
                   │  con datos CONAGUA     │
                   └────────────────────────┘
```

---

## El LLM de ConAIgua: Modelo Propio Entrenado desde Cero

### ¿Por qué un LLM propio?

A diferencia de sistemas que utilizan modelos genéricos (OpenAI, Anthropic, Meta, etc.), ConAIgua desarrolla su propio modelo de lenguaje entrenado exclusivamente con datos meteorológicos mexicanos. Esto permite:

- **Especialización total en el dominio**: El modelo comprende de forma nativa las estaciones CONAGUA, sus identificadores, regiones climáticas y patrones históricos de México
- **Privacidad y soberanía de datos**: No se envía información a servicios externos
- **Control total del modelo**: Ajuste fino, versionado y despliegue completamente controlados
- **Sin dependencia de terceros**: No hay costos por API ni riesgos de discontinuidad de servicio

### Pipeline de Entrenamiento del LLM

```
┌─────────────────────────────────────────────────────────────────┐
│              PIPELINE DE ENTRENAMIENTO CONAIGU LLM              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. INGESTA DE DATOS                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Dataset CONAGUA (CSV/Parquet)                          │    │
│  │  • Estaciones meteorológicas (todo México)              │    │
│  │  • Series históricas: temperatura, precipitación,       │    │
│  │    humedad, viento, presión atmosférica                 │    │
│  │  • Metadata: coordenadas, altitud, estado, municipio    │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  2. PREPROCESAMIENTO                                            │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Pipeline de Limpieza y Normalización (Polars/Pandas)   │    │
│  │  • Manejo de valores nulos e interpolación              │    │
│  │  • Normalización de unidades y escalas                  │    │
│  │  • Detección y corrección de outliers                   │    │
│  │  • Tokenización de series temporales                    │    │
│  │  • Conversión a formato texto estructurado              │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  3. CONSTRUCCIÓN DEL CORPUS                                     │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Generación de Corpus de Entrenamiento                  │    │
│  │  • Pares (pregunta, respuesta) sintéticos               │    │ 
│  │  • Resúmenes descriptivos de series meteorológicas      │    │ 
│  │  • Contexto geográfico y temporal enriquecido           │    │
│  │  • Vocabulario especializado del dominio climático MX   │    │ 
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  4. ENTRENAMIENTO DEL MODELO                                    │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Arquitectura Transformer (desde cero)                  │    │
│  │  • Pre-entrenamiento: Modelado de lenguaje causal (CLM) │    │
│  │  • Fine-tuning supervisado: pares Q&A meteorológicos    │    │
│  │  • RLHF opcional: feedback humano sobre respuestas      │    │
│  │  • Framework: PyTorch + HuggingFace Trainer (interno)   │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  5. EVALUACIÓN Y VALIDACIÓN                                     │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Métricas de Calidad                                    │    │
│  │  • Perplexity sobre corpus de validación CONAGUA        │    │
│  │  • BLEU / ROUGE en respuestas de referencia             │    │
│  │  • Evaluación humana de precisión meteorológica         │    │
│  │  • Benchmarks de latencia y throughput                  │    │ 
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  6. DESPLIEGUE                                                  │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Serving del Modelo                                     │    │
│  │  • Exportación a ONNX o TorchScript                     │    │
│  │  • Quantización INT8/FP16 para eficiencia               │    │
│  │  • Serving via API REST interna (Rust ↔ Python bridge)  │    │
│  │  • Versionado de modelos con MLflow                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Estructura del Dataset CONAGUA

| Campo | Descripción | Tipo |
|---|---|---|
| `station_id` | Identificador único de estación | String |
| `state` | Estado de la República Mexicana | String |
| `municipality` | Municipio de la estación | String |
| `latitude / longitude` | Coordenadas geográficas | Float |
| `altitude_m` | Altitud sobre el nivel del mar | Float |
| `date` | Fecha de la observación | Date |
| `temp_max_c` | Temperatura máxima (°C) | Float |
| `temp_min_c` | Temperatura mínima (°C) | Float |
| `temp_avg_c` | Temperatura promedio (°C) | Float |
| `precipitation_mm` | Precipitación acumulada (mm) | Float |
| `humidity_pct` | Humedad relativa (%) | Float |
| `wind_speed_kmh` | Velocidad del viento (km/h) | Float |
| `wind_direction` | Dirección del viento | String |
| `atmospheric_pressure_hpa` | Presión atmosférica (hPa) | Float |
| `evaporation_mm` | Evaporación (mm) | Float |

### Pipelines de Datos

```
┌──────────────────────────────────────────────────────────────┐
│                    PIPELINES DE DATOS                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Pipeline 1: ETL (Extract, Transform, Load)                  │
│  ┌────────────┐   ┌──────────────┐   ┌──────────────────┐    │
│  │ Raw CSV    │ → │  Polars      │ → │  PostgreSQL /    │    │
│  │ CONAGUA    │   │  Transform   │   │  Parquet Store   │    │
│  └────────────┘   └──────────────┘   └──────────────────┘    │
│                                                              │
│  Pipeline 2: Embedding para RAG                              │
│  ┌────────────┐   ┌──────────────┐   ┌──────────────────┐    │
│  │ Datos      │ → │  Tokenizer   │ → │  Qdrant Vector   │    │
│  │ limpios    │   │  + Encoder   │   │  DB (embeddings) │    │
│  └────────────┘   └──────────────┘   └──────────────────┘    │
│                                                              │
│  Pipeline 3: Entrenamiento continuo                          │
│  ┌────────────┐   ┌──────────────┐   ┌──────────────────┐    │
│  │ Nuevos     │ → │  Fine-tuning │ → │  Model Registry  │    │
│  │ datos      │   │  incremental │   │  (MLflow)        │    │
│  └────────────┘   └──────────────┘   └──────────────────┘    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Características Principales

### Inteligencia Artificial
- **LLM Propio (ConAIgua Model)**: Modelo Transformer entrenado desde cero con datos CONAGUA — sin dependencia de APIs externas
- **RAG (Retrieval-Augmented Generation)**: Búsqueda semántica en dataset CONAGUA para enriquecer respuestas con datos precisos
- **Embeddings Vectoriales**: Qdrant para búsqueda eficiente de contexto meteorológico
- **Streaming de Respuestas**: WebSocket para respuestas en tiempo real
- **Entrenamiento Continuo**: Pipeline para re-entrenamiento con nuevos datos CONAGUA

### Frontend (React + Next.js)
- **Server-Side Rendering (SSR)**: Carga inicial rápida y SEO optimizado
- **Static Site Generation (SSG)**: Páginas estáticas para contenido no dinámico
- **App Router**: Enrutamiento moderno con layouts anidados (Next.js 14+)
- **React Server Components**: Reducción del bundle JS en el cliente
- **API Routes**: Backend-for-Frontend integrado en Next.js

### Datos Meteorológicos
- **Dataset CONAGUA**: Datos históricos de estaciones meteorológicas de toda la República Mexicana
- **Múltiples Métricas**: Temperatura, precipitación, humedad, viento, presión, evaporación
- **Consultas Temporales**: Rangos de fechas, agregaciones, tendencias y anomalías

### Seguridad
- **Microsegmentación**: Aislamiento de componentes con Network Policies
- **Zero Trust Architecture**: Autenticación y autorización en cada capa
- **Cifrado**: TLS 1.3 en tránsito, AES-256 en reposo
- **JWT Authentication**: Tokens RS256 con rotación automática
- **WAF**: Protección contra OWASP Top 10
- **Auditoría**: Logging completo con integración SIEM

### Performance
- **Cache Inteligente**: Redis para sesiones y resultados frecuentes
- **Async/Await**: Backend completamente asíncrono en Rust
- **Connection Pooling**: Optimización de conexiones a bases de datos
- **Rate Limiting**: Prevención de abuso
- **Model Quantization**: INT8/FP16 para inferencia eficiente del LLM propio

---

## Arquitectura del Sistema

### Arquitectura Hexagonal (Ports & Adapters)

El proyecto sigue los principios de **Arquitectura Hexagonal** (también conocida como Ports and Adapters), lo que garantiza:

- **Separación de Concerns**: Lógica de negocio independiente de frameworks
- **Testabilidad**: Fácil creación de tests unitarios y de integración
- **Flexibilidad**: Cambio de tecnologías sin afectar la lógica core
- **Mantenibilidad**: Código organizado y escalable

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
│  │  │        • ConAIguaLLMService (modelo propio)    │  │   │
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
│  │  │ (modelo propio,      │  │ (Polars/Pandas)    │    │   │
│  │  │  servido localmente) │  │                    │    │   │
│  │  └──────────────────────┘  └────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Ventajas de esta Arquitectura

1. **Domain-Driven Design (DDD)**: La lógica de negocio es el núcleo
2. **Dependency Inversion**: Las dependencias apuntan hacia el dominio
3. **Plug & Play**: Fácil versionado del LLM propio sin afectar la lógica de negocio
4. **Testing**: Mocks simples de puertos para testing unitario
5. **Clean Code**: Separación clara de responsabilidades

### Microsegmentación y Seguridad

El sistema implementa **microsegmentación** siguiendo el modelo **Zero Trust**:

```
┌───────────────────────────────────────────────────────────┐
│  SEGMENTO 1: Autenticación                                │
│  • Auth Service, Session Manager                          │
│  • Acceso: PostgreSQL:5432, Redis:6379                    │
│  • Bloqueado: MongoDB, Qdrant, LLM Service, Internet      │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│  SEGMENTO 2: Backend Services                             │
│  • Chat Orchestrator, RAG, ConAIgua LLM Service           │
│  • Acceso: MongoDB:27017, Qdrant:6333, LLM Service:8080   │
│  • Bloqueado: PostgreSQL (solo Auth puede), Internet      │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│  SEGMENTO 3: LLM Inference                                │
│  • ConAIgua Model Server (PyTorch / ONNX Runtime)         │
│  • Acceso: Solo desde Backend Services                    │
│  • Sin acceso a Internet ni a bases de datos              │
└───────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│  SEGMENTO 4: Data Layer                                   │
│  • PostgreSQL, MongoDB, Qdrant, Redis                     │
│  • Firewall interno con IP whitelisting                   │
│  • Acceso: Solo servicios autorizados por puerto          │
└───────────────────────────────────────────────────────────┘
```

**Implementación**: Kubernetes Network Policies o AWS Security Groups

### Diagramas C4

El proyecto incluye documentación completa siguiendo el modelo **C4** (Context, Containers, Components, Code):

- **Nivel 1 - Contexto**: Vista general del sistema y actores
- **Nivel 2 - Contenedores**: Aplicaciones y bases de datos
- **Nivel 3 - Componentes**: Detalle interno del API Backend y del pipeline LLM
- **Vista de Datos**: Estructura de almacenamiento y dataset CONAGUA
- **Vista de Seguridad**: Capas de seguridad y microsegmentación

Ver carpeta `/docs/architecture/` para diagramas completos.

### Bases de Datos

| Tecnología | Uso | Tipo |
|---|---|---|
| **PostgreSQL** | Usuarios, sesiones, auditoría | Relacional |
| **MongoDB** | Historial de conversaciones | Documental |
| **Qdrant** | Embeddings vectoriales (RAG) | Vectorial |
| **Redis** | Cache, rate limiting | En memoria |

### Stack Tecnológico Completo

| Capa | Tecnología | Notas |
|---|---|---|
| **Frontend** | React 18 + Next.js 14 | App Router, SSR, RSC |
| **Backend API** | Rust (Axum) | Async, alto rendimiento |
| **LLM** | PyTorch + Transformer propio | Entrenado desde cero con CONAGUA |
| **RAG** | Qdrant + embeddings propios | Vectores del modelo ConAIgua |
| **Data Pipeline** | Polars / Pandas | ETL del dataset CONAGUA |
| **Model Serving** | ONNX Runtime / TorchServe | Inferencia optimizada local |
| **BD Relacional** | PostgreSQL | Usuarios y sesiones |
| **BD Documental** | MongoDB | Historial de chat |
| **Cache** | Redis | Sesiones y rate limiting |
| **Infraestructura** | Docker + Kubernetes | Contenedorización y orquestación |
| **Reverse Proxy** | Nginx | Load balancing y TLS |
| **MLOps** | MLflow | Versionado del modelo LLM |

### Infraestructura

- **Docker** + **Docker Compose**: Contenedorización
- **Kubernetes** (opcional): Orquestación y Network Policies
- **Nginx**: Reverse proxy y load balancing
- **Let's Encrypt**: Certificados SSL/TLS
- **MLflow**: Registry y versionado del modelo ConAIgua LLM

---

## Seguridad

### Controles Implementados

#### Capa de Red
- Firewall perimetral con IPS/IDS
- WAF (Web Application Firewall)
- DDoS protection
- TLS 1.3 obligatorio
- Geo-blocking opcional

#### Autenticación y Autorización
- JWT con RS256 (asimétrico)
- Argon2 para passwords (cost factor 12)
- Refresh token rotation
- RBAC (Role-Based Access Control)
- Session timeout configurable
- MFA opcional (TOTP)

#### Protección de Aplicación
- Input sanitization
- SQL/NoSQL injection prevention
- XSS protection (CSP headers)
- CSRF tokens
- Rate limiting por usuario/IP
- Request size limits

#### Datos
- Encryption at rest (AES-256)
- Encryption in transit (TLS)
- Secrets management (Vault/AWS Secrets)
- Backup encryption
- Data masking en logs

#### Microsegmentación
- Network Policies (K8s) o Security Groups (AWS)
- Aislamiento por segmento (incluyendo segmento dedicado para el LLM)
- Default Deny
- Least privilege access

### Auditoría y Compliance
- Logging estructurado (JSON)
- SIEM integration
- Alertas de seguridad
- Compliance: GDPR, SOC2

---

## License

Copyright © 2026 Chris6264

Licensed under the Apache License, Version 2.0.
