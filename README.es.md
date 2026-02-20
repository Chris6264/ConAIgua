<div align="center">

# ConAIgua - Sistema de Consultas Hidrometeorólogicas con LLM

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Rust](https://img.shields.io/badge/Rust-1.75+-orange.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow.svg)

[English Version](README.md)

</div>

Chatbot inteligente para consultar datos hidrometeorológicos históricos de CONAGUA (Comisión Nacional del Agua de México) mediante procesamiento de lenguaje natural, impulsado por un **LLM entrenado desde cero** con datos exclusivos de CONAGUA.

## Descripción General

**ConAIgua** es un sistema de consulta de datos hidrometeorológicos que utiliza un **Large Language Model (LLM) propio**, entrenado íntegramente desde cero con datos históricos de CONAGUA (Comisión Nacional del Agua de México), combinado con **Retrieval-Augmented Generation (RAG)** para proporcionar respuestas precisas y contextuales en lenguaje natural.

> **Importante**: El modelo de lenguaje utilizado en ConAIgua **no es un LLM externo ni preexistente** (no es GPT, Claude, LLaMA, ni ningún modelo de terceros). Es un modelo **diseñado, entrenado y optimizado desde cero** utilizando exclusivamente el dataset de CONAGUA, pipelines de procesamiento de datos hidrometeorológicos y arquitecturas Transformer propias. Esto garantiza que el modelo tenga conocimiento profundo y especializado del dominio climatológico mexicano.

### ¿Qué problema resuelve?

Los datos hidrometeorológicos históricos suelen estar en formatos poco accesibles (archivos TXT planos, CSVs, bases de datos complejas). Este chatbot permite:

- **Consultas en lenguaje natural**: "¿Cuál fue la temperatura máxima en Culiacán en enero de 1978?"
- **Análisis de datos climatológicos**: Precipitación, evaporación, temperatura máxima y mínima diaria
- **Búsqueda semántica**: RAG sobre el dataset CONAGUA para respuestas contextuales precisas
- **Respuestas en tiempo real**: Interfaz web interactiva con streaming de respuestas
- **Dominio especializado**: El LLM comprende de forma nativa la estructura de estaciones CONAGUA, sus identificadores, estados y municipios de México

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
    │  (Usuarios/   │     │  (Historial │     │   (Base de  │
    │  Sesiones)    │     │   de Chat)  │     │  Vectores)  │
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

A diferencia de sistemas que utilizan modelos genéricos (OpenAI, Anthropic, Meta, etc.), ConAIgua desarrolla su propio modelo de lenguaje entrenado exclusivamente con datos hidrometeorológicos mexicanos. Esto permite:

- **Especialización total en el dominio**: El modelo comprende de forma nativa las estaciones CONAGUA, sus claves, organismos responsables, estados y municipios de México
- **Privacidad y soberanía de datos**: No se envía información a servicios externos
- **Control total del modelo**: Ajuste fino, versionado y despliegue completamente controlados
- **Sin dependencia de terceros**: No hay costos por API ni riesgos de discontinuidad de servicio

### Formato Real del Dataset CONAGUA

El dataset proviene de la **Base de Datos Climatológica Nacional** (CNA-SMN-CG-GMC-SMAA-CLIMATOLOGIA), con datos suministrados por las Oficinas Regionales de CONAGUA. Cada archivo de estación tiene el siguiente formato:

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

### Estructura del Dataset CONAGUA

**Metadatos de Estación:**

| Campo | Descripción | Ejemplo |
|---|---|---|
| `ESTACION` | Clave única de la estación | `25164` |
| `NOMBRE` | Nombre de la estación | `ALTO DE CULIACANCITO` |
| `ESTADO` | Estado de la República Mexicana | `SINALOA` |
| `MUNICIPIO` | Municipio de la estación | `CULIACAN` |
| `SITUACIÓN` | Estado operativo | `SUSPENDIDA` / `ACTIVA` |
| `ORGANISMO` | Organismo responsable | `CONAGUA-DGE` |
| `CVE-OMM` | Clave OMM internacional | `Nulo` o código numérico |
| `LATITUD` | Coordenada geográfica | `024.807°` |
| `LONGITUD` | Coordenada geográfica | `-107.555°` |
| `ALTITUD` | Metros sobre el nivel del mar | `24 msnm` |
| `EMISION` | Fecha de emisión del reporte | `06/04/2020` |

**Registros Diarios:**

| Campo | Descripción | Unidad |
|---|---|---|
| `FECHA` | Fecha de la observación | `DD/MM/YYYY` |
| `PRECIP` | Precipitación acumulada | mm |
| `EVAP` | Evaporación | mm |
| `TMAX` | Temperatura máxima del día | °C |
| `TMIN` | Temperatura mínima del día | °C |

### Pipeline de Entrenamiento del LLM

```
┌─────────────────────────────────────────────────────────────────┐
│              PIPELINE DE ENTRENAMIENTO ConAIgua LLM             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. INGESTA DE DATOS                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Dataset CONAGUA (archivos TXT planos por estación)     │    │
│  │  • Metadatos: clave, nombre, estado, municipio,         │    │
│  │    situación, organismo, coordenadas, altitud           │    │
│  │  • Series diarias: PRECIP, EVAP, TMAX, TMIN             │    │
│  │  • Cobertura histórica desde los años 1920 hasta 2020   │    │
│  │  • Miles de estaciones en toda la República Mexicana    │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  2. PREPROCESAMIENTO                                            │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Pipeline de Limpieza y Normalización (Polars/Pandas)   │    │
│  │  • Parseo del formato TXT propietario de CONAGUA        │    │
│  │  • Tratamiento del literal "Nulo" → NaN                 │    │
│  │  • Interpolación temporal de valores faltantes          │    │
│  │  • Detección y corrección de outliers climatológicos    │    │
│  │  • Normalización de coordenadas y altitudes             │    │
│  │  • Conversión a formato tabular estructurado            │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  3. CONSTRUCCIÓN DEL CORPUS                                     │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Generación de Corpus de Entrenamiento                  │    │
│  │  • Pares (pregunta, respuesta) sintéticos               │    │
│  │    ej: "TMAX en estación 25164 el 09/01/1978?" → "31°C" │    │
│  │  • Resúmenes mensuales y anuales por estación           │    │
│  │  • Contexto geográfico enriquecido (estado, municipio)  │    │
│  │  • Vocabulario de terminología CONAGUA y climatológica  │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  4. ENTRENAMIENTO DEL MODELO                                    │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Arquitectura Transformer (desde cero)                  │    │
│  │  • Pre-entrenamiento: Modelado de lenguaje causal (CLM) │    │
│  │  • Fine-tuning supervisado: pares Q&A climatológicos    │    │ 
│  │  • RLHF opcional: feedback humano sobre respuestas      │    │
│  │  • Framework: PyTorch + HuggingFace Trainer (interno)   │    │ 
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                   │
│  5. EVALUACIÓN Y VALIDACIÓN                                     │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Métricas de Calidad                                    │    │
│  │  • Perplexity sobre corpus de validación CONAGUA        │    │
│  │  • BLEU / ROUGE en respuestas de referencia             │    │
│  │  • Evaluación humana de precisión climatológica         │    │
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

### Pipelines de Datos

```
┌──────────────────────────────────────────────────────────────┐
│                    PIPELINES DE DATOS                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Pipeline 1: ETL (Extract, Transform, Load)                  │
│  ┌────────────┐   ┌──────────────┐   ┌──────────────────┐    │
│  │ TXT plano  │ → │  Polars      │ → │  PostgreSQL /    │    │
│  │ CONAGUA    │   │  Transform   │   │  Parquet Store   │    │
│  └────────────┘   └──────────────┘   └──────────────────┘    │
│                                                              │
│  Pipeline 2: Embedding para RAG                              │
│  ┌────────────┐   ┌──────────────┐   ┌──────────────────┐    │
│  │ Datos      │ → │  Tokenizer   │ → │  Qdrant Vector   │    │
│  │ limpios    │   │  + Encoder   │   │  DB (embeddings) │    │
│  └────────────┘   └──────────────┘   └──────────────────┘    │
│                                                              │
│  Pipeline 3: Entrenamiento Continuo                          │
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
- **RAG (Retrieval-Augmented Generation)**: Búsqueda semántica en el dataset CONAGUA para enriquecer respuestas con datos precisos
- **Embeddings Vectoriales**: Qdrant para búsqueda eficiente de contexto climatológico
- **Streaming de Respuestas**: WebSocket para respuestas en tiempo real
- **Entrenamiento Continuo**: Pipeline para re-entrenamiento con nuevos datos CONAGUA

### Frontend (React + Next.js)
- **Server-Side Rendering (SSR)**: Carga inicial rápida y SEO optimizado
- **Static Site Generation (SSG)**: Páginas estáticas para contenido no dinámico
- **App Router**: Enrutamiento moderno con layouts anidados (Next.js 14+)
- **React Server Components**: Reducción del bundle JS en el cliente
- **API Routes**: Backend-for-Frontend integrado en Next.js

### Datos Climatológicos
- **Dataset CONAGUA**: Base de Datos Climatológica Nacional con registros diarios desde los años 1920
- **4 Variables Climáticas**: Precipitación (mm), Evaporación (mm), Temperatura Máxima (°C), Temperatura Mínima (°C)
- **Miles de Estaciones**: Cobertura de toda la República Mexicana
- **Consultas Temporales**: Rangos de fechas, agregaciones mensuales/anuales, tendencias y anomalías

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
│  │              ADAPTADORES (Infraestructura)           │   │
│  │                                                      │   │
│  │   ┌─────────────┐          ┌─────────────┐           │   │
│  │   │  REST API   │          │  WebSocket  │           │   │
│  │   │   (Axum)    │          │   (Axum)    │           │   │
│  │   └──────┬──────┘          └──────┬──────┘           │   │
│  └─────────┼────────────────────────│───────────────────┘   │
│            │                        │                       │
│            │      PUERTOS PRIMARIOS (Entrada)               │
│            ▼                        ▼                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   NÚCLEO DE DOMINIO                  │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │     Servicios de Aplicación (Casos de Uso)     │  │   │  
│  │  │       • ChatOrchestrator                       │  │   │
│  │  │       • AuthenticationService                  │  │   │
│  │  │       • SessionManager                         │  │   │ 
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │      Lógica de Dominio (Reglas de Negocio)     │  │   │
│  │  │        • IntentParser                          │  │   │ 
│  │  │        • RAGService                            │  │   │
│  │  │        • ConAIguaLLMService (modelo propio)    │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │        Entidades de Dominio (Modelos)          │  │   │
│  │  │        • User, Session, Message                │  │   │
│  │  │        • ChatContext, EmbeddingVector          │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └───────────────────────┬──────────────────────────────┘   │
│                          │                                  │
│            PUERTOS SECUNDARIOS (Salida)                     │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ADAPTADORES (Infraestructura)           │   │
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
2. **Inversión de Dependencias**: Las dependencias apuntan hacia el dominio
3. **Plug & Play**: Fácil versionado del LLM propio sin afectar la lógica de negocio
4. **Testing**: Mocks simples de puertos para testing unitario
5. **Código Limpio**: Separación clara de responsabilidades

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
│  SEGMENTO 4: Capa de Datos                                │
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
| **Data Pipeline** | Polars / Pandas | ETL del dataset CONAGUA (TXT → tabular) |
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
- Protección DDoS
- TLS 1.3 obligatorio
- Geo-blocking opcional

#### Autenticación y Autorización
- JWT con RS256 (asimétrico)
- Argon2 para contraseñas (cost factor 12)
- Rotación de refresh tokens
- RBAC (Control de Acceso Basado en Roles)
- Session timeout configurable
- MFA opcional (TOTP)

#### Protección de Aplicación
- Sanitización de entradas
- Prevención de inyección SQL/NoSQL
- Protección XSS (cabeceras CSP)
- Tokens CSRF
- Rate limiting por usuario/IP
- Límites de tamaño de solicitudes

#### Datos
- Cifrado en reposo (AES-256)
- Cifrado en tránsito (TLS)
- Gestión de secretos (Vault / AWS Secrets)
- Cifrado de backups
- Enmascaramiento de datos en logs

#### Microsegmentación
- Network Policies (K8s) o Security Groups (AWS)
- Aislamiento por segmento (incluyendo segmento dedicado para el LLM)
- Denegación por defecto
- Principio de mínimo privilegio

### Auditoría y Compliance
- Logging estructurado (JSON)
- Integración SIEM
- Alertas de seguridad
- Compliance: GDPR, SOC2

---

## Licencia

Copyright © 2026 Chris6264

Licenciado bajo la Licencia Apache, Versión 2.0.
