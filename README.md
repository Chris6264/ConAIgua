# ConAIgua - Sistema de Consultas Meteorológicas con LLM

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Rust](https://img.shields.io/badge/Rust-1.75+-orange.svg)
![Svelte](https://img.shields.io/badge/Svelte-4.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow.svg)

Chatbot inteligente que permite consultar información meteorológica histórica de CONAGUA mediante procesamiento de lenguaje natural.

</div>

## Descripción General

**ConAIgua** es un sistema de consulta de información meteorológica que utiliza **Large Language Models (LLM)** y **Retrieval-Augmented Generation (RAG)** para proporcionar respuestas en lenguaje natural sobre datos históricos de CONAGUA (Comisión Nacional del Agua de México).

### ¿Qué problema resuelve?

Los datos meteorológicos históricos suelen estar en formatos poco accesibles (CSVs, bases de datos complejas). Este chatbot permite:
- **Consultas en lenguaje natural**: "¿Cuál fue la temperatura en Culiacán la semana pasada?"
- **Análisis de datos meteorológicos**: Temperaturas, precipitación, humedad, viento, presión atmosférica
- **Búsqueda semántica**: RAG sobre dataset CONAGUA para respuestas contextuales precisas
- **Respuestas en tiempo real**: Interfaz web interactiva con streaming de respuestas

### Arquitectura de Alto Nivel

```
┌─────────────┐      HTTPS/WSS      ┌──────────────┐
│   Frontend  │ ◄─────────────────► │ API Backend  │
│   (Svelte)  │                     │    (Rust)    │
└─────────────┘                     └───────┬──────┘
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
                    ▼                       ▼                       ▼
            ┌───────────────┐       ┌─────────────┐       ┌─────────────┐
            │   PostgreSQL  │       │   MongoDB   │       │   Qdrant    │
            │   (Users/     │       │  (Chat      │       │  (Vector    │
            │   Sessions)   │       │  History)   │       │    DB)      │
            └───────────────┘       └─────────────┘       └─────────────┘
                                                                │
                                                                ▼
                                                          ┌─────────────┐
                                                          │ LLM Provider│
                                                          │ (OpenAI/    │
                                                          │ Anthropic)  │
                                                          └─────────────┘
```

---

## Características Principales

### Inteligencia Artificial
- **LLM Integration**: Soporte para OpenAI, Anthropic Claude, y modelos locales
- **RAG (Retrieval-Augmented Generation)**: Búsqueda semántica en dataset CONAGUA
- **Embeddings Vectoriales**: Qdrant para búsqueda eficiente de contexto
- **Streaming de Respuestas**: WebSocket para respuestas en tiempo real

### Datos Meteorológicos
- **Dataset CONAGUA**: Datos históricos de estaciones meteorológicas mexicanas
- **Múltiples Métricas**: Temperatura, precipitación, humedad, viento, presión
- **Consultas Temporales**: Rangos de fechas, agregaciones, tendencias

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
│                    HEXAGONAL ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ADAPTERS (Infrastructure)               │   │
│  │                                                      │   │
│  │  ┌─────────────┐              ┌─────────────┐        │   │
│  │  │   REST API  │              │  WebSocket  │        │   │
│  │  │  (Axum)     │              │   (Axum)    │        │   │
│  │  └──────┬──────┘              └──────┬──────┘        │   │
│  └─────────┼────────────────────────────│───────────────┘   │
│            │                            │                   │                            
│            │    PRIMARY PORTS (Input)   │                   │  
│            ▼                            ▼                   │            
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   DOMAIN CORE                        │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │         Application Services (Use Cases)       │  │   │
│  │  │  • ChatOrchestrator                            │  │   │
│  │  │  • AuthenticationService                       │  │   │
│  │  │  • SessionManager                              │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │           Domain Logic (Business Rules)        │  │   │
│  │  │  • IntentParser                                │  │   │
│  │  │  • RAGService                                  │  │   │
│  │  │  • LLMService                                  │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │        Domain Entities (Models)                │  │   │
│  │  │  • User, Session, Message                      │  │   │                   
│  │  │  • ChatContext, EmbeddingVector                │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └───────────────────────┬──────────────────────────────┘   │
│                          │                                  │
│            SECONDARY PORTS (Output)                         │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ADAPTERS (Infrastructure)               │   │
│  │                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐  │   │
│  │  │PostgreSQL│  │ MongoDB  │  │  Qdrant  │  │Redis │  │   │
│  │  │Repository│  │Repository│  │Repository│  │Cache │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────┘  │   │
│  │                                                      │   │
│  │  ┌──────────────────┐  ┌──────────────────────────┐  │   │
│  │  │  LLM HTTP Client │  │  CONAGUA DataFrame       │  │   │
│  │  │  (OpenAI/Claude) │  │  (Polars/Pandas)         │  │   │
│  │  └──────────────────┘  └──────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Ventajas de esta Arquitectura

1. **Domain-Driven Design (DDD)**: La lógica de negocio es el núcleo
2. **Dependency Inversion**: Las dependencias apuntan hacia el dominio
3. **Plug & Play**: Fácil cambio de PostgreSQL a MySQL, o de OpenAI a Claude
4. **Testing**: Mocks simples de puertos para testing unitario
5. **Clean Code**: Separación clara de responsabilidades

### Microsegmentación y Seguridad

El sistema implementa **microsegmentación** siguiendo el modelo **Zero Trust**:

```
┌───────────────────────────────────────────────────────────┐
│  SEGMENTO 1: Autenticación                                │
│  • Auth Service, Session Manager                          │
│  • Acceso: PostgreSQL:5432, Redis:6379                    │
│  • Bloqueado: MongoDB, Qdrant, Internet                   │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  SEGMENTO 2: Backend Services                             │
│  • Chat Orchestrator, RAG, LLM                            │
│  • Acceso: MongoDB:27017, Qdrant:6333, LLM Provider:443   │
│  • Bloqueado: PostgreSQL (solo Auth puede)                │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  SEGMENTO 3: Data Layer                                   │
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
- **Nivel 3 - Componentes**: Detalle interno del API Backend
- **Vista de Datos**: Estructura de almacenamiento
- **Vista de Seguridad**: Capas de seguridad y microsegmentación

Ver carpeta `/docs/architecture/` para diagramas completos.

### Bases de Datos

| Tecnología | Uso | Tipo |
|-----------|-----|------|
| **PostgreSQL** | Usuarios, sesiones, auditoría | Relacional |
| **MongoDB** | Historial de conversaciones | Documental |
| **Qdrant** | Embeddings vectoriales (RAG) | Vectorial |
| **Redis** | Cache, rate limiting | En memoria |

### Infrastructura

- **Docker** + **Docker Compose**: Contenedorización
- **Kubernetes** (opcional): Orquestación y Network Policies
- **Nginx**: Reverse proxy y load balancing
- **Let's Encrypt**: Certificados SSL/TLS

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
- Aislamiento por segmento
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
