# Agente Inteligente LLM --- Residencia
# 🌦️ Weather Chatbot - Sistema de Consultas Meteorológicas con LLM

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Rust](https://img.shields.io/badge/Rust-1.75+-orange.svg)
![Svelte](https://img.shields.io/badge/Svelte-4.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow.svg)

Chatbot inteligente que permite consultar información meteorológica histórica de CONAGUA mediante procesamiento de lenguaje natural.

[Características](#-características) • [Arquitectura](#-arquitectura) • [Instalación](#-instalación) • [Uso](#-uso) • [Documentación](#-documentación)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
  - [Arquitectura Hexagonal](#arquitectura-hexagonal-ports--adapters)
  - [Microsegmentación](#microsegmentación-y-seguridad)
  - [Diagrama C4](#diagramas-c4)
- [Stack Tecnológico](#-stack-tecnológico)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso](#-uso)
- [Seguridad](#-seguridad)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🎯 Descripción General

El **Weather Chatbot** es un sistema de consulta de información meteorológica que utiliza **Large Language Models (LLM)** y **Retrieval-Augmented Generation (RAG)** para proporcionar respuestas en lenguaje natural sobre datos históricos de CONAGUA (Comisión Nacional del Agua de México).

### ¿Qué problema resuelve?

Los datos meteorológicos históricos suelen estar en formatos poco accesibles (CSVs, bases de datos complejas). Este chatbot permite:
- 💬 **Consultas en lenguaje natural**: "¿Cuál fue la temperatura en Culiacán la semana pasada?"
- 📊 **Análisis de datos meteorológicos**: Temperaturas, precipitación, humedad, viento, presión atmosférica
- 🔍 **Búsqueda semántica**: RAG sobre dataset CONAGUA para respuestas contextuales precisas
- 🚀 **Respuestas en tiempo real**: Interfaz web interactiva con streaming de respuestas

### Arquitectura de Alto Nivel

```
┌─────────────┐      HTTPS/WSS     ┌──────────────┐
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

## ✨ Características Principales

### 🤖 Inteligencia Artificial
- **LLM Integration**: Soporte para OpenAI, Anthropic Claude, y modelos locales
- **RAG (Retrieval-Augmented Generation)**: Búsqueda semántica en dataset CONAGUA
- **Embeddings Vectoriales**: Qdrant para búsqueda eficiente de contexto
- **Streaming de Respuestas**: WebSocket para respuestas en tiempo real

### 📊 Datos Meteorológicos
- **Dataset CONAGUA**: Datos históricos de estaciones meteorológicas mexicanas
- **Múltiples Métricas**: Temperatura, precipitación, humedad, viento, presión
- **Consultas Temporales**: Rangos de fechas, agregaciones, tendencias
- **Ubicaciones**: Búsqueda por estado, ciudad, o estación específica

### 🔐 Seguridad
- **Microsegmentación**: Aislamiento de componentes con Network Policies
- **Zero Trust Architecture**: Autenticación y autorización en cada capa
- **Cifrado**: TLS 1.3 en tránsito, AES-256 en reposo
- **JWT Authentication**: Tokens RS256 con rotación automática
- **WAF**: Protección contra OWASP Top 10
- **Auditoría**: Logging completo con integración SIEM

### ⚡ Performance
- **Cache Inteligente**: Redis para sesiones y resultados frecuentes
- **Async/Await**: Backend completamente asíncrono en Rust
- **Connection Pooling**: Optimización de conexiones a bases de datos
- **Rate Limiting**: Prevención de abuso

---

## 🏗️ Arquitectura del Sistema

### Arquitectura Hexagonal (Ports & Adapters)

El proyecto sigue los principios de **Arquitectura Hexagonal** (también conocida como Ports and Adapters), lo que garantiza:

- ✅ **Separación de Concerns**: Lógica de negocio independiente de frameworks
- ✅ **Testabilidad**: Fácil creación de tests unitarios y de integración
- ✅ **Flexibilidad**: Cambio de tecnologías sin afectar la lógica core
- ✅ **Mantenibilidad**: Código organizado y escalable

```
┌─────────────────────────────────────────────────────────────┐
│                    HEXAGONAL ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              ADAPTERS (Infrastructure)               │  │
│  │                                                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │   REST API  │  │  WebSocket  │  │   GraphQL   │  │  │
│  │  │  (Axum)     │  │   (Axum)    │  │  (Future)   │  │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │  │
│  └─────────┼────────────────┼────────────────┼─────────┘  │
│            │                │                │             │
│            │    PRIMARY PORTS (Input)        │             │
│            ▼                ▼                ▼             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   DOMAIN CORE                        │  │
│  │                                                       │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │         Application Services (Use Cases)       │  │  │
│  │  │  • ChatOrchestrator                            │  │  │
│  │  │  • AuthenticationService                       │  │  │
│  │  │  • SessionManager                              │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │           Domain Logic (Business Rules)        │  │  │
│  │  │  • WeatherIntentParser                         │  │  │
│  │  │  • RAGService                                   │  │  │
│  │  │  • LLMService                                   │  │  │
│  │  │  • WeatherQueryService                         │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │        Domain Entities (Models)                │  │  │
│  │  │  • User, Session, Message                      │  │  │
│  │  │  • WeatherData, Location                       │  │  │
│  │  │  • ChatContext, EmbeddingVector                │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └───────────────────────┬───────────────────────────────┘  │
│                          │                                  │
│            SECONDARY PORTS (Output)                         │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              ADAPTERS (Infrastructure)               │  │
│  │                                                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐ │  │
│  │  │PostgreSQL│  │ MongoDB  │  │  Qdrant  │  │Redis │ │  │
│  │  │Repository│  │Repository│  │Repository│  │Cache │ │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────┘ │  │
│  │                                                       │  │
│  │  ┌──────────────────┐  ┌──────────────────────────┐  │  │
│  │  │  LLM HTTP Client │  │  CONAGUA DataFrame       │  │  │
│  │  │  (OpenAI/Claude) │  │  (Polars/Pandas)         │  │  │
│  │  └──────────────────┘  └──────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
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
│  • Chat Orchestrator, RAG, LLM, Weather Query             │
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

📁 Ver carpeta `/docs/architecture/` para diagramas completos.

---

## 🛠️ Stack Tecnológico

### Backend (Rust)

```toml
# Core Framework
axum = "0.7"              # Web framework
tokio = "1"               # Async runtime
tower = "0.4"             # Middleware

# Databases
sqlx = "0.7"              # PostgreSQL (async)
mongodb = "2.8"           # MongoDB driver
qdrant-client = "1.7"     # Vector DB
redis = "0.24"            # Cache

# LLM & AI
reqwest = "0.11"          # HTTP client for LLM APIs
serde = "1.0"             # Serialization

# Security
jsonwebtoken = "9.0"      # JWT
bcrypt = "0.15"           # Password hashing
argon2 = "0.5"            # Alternative hashing

# Logging & Monitoring
tracing = "0.1"           # Structured logging
tracing-subscriber = "0.3"
prometheus = "0.13"       # Metrics

# Data Processing
polars = "0.36"           # DataFrame (alternativa: pandas)
```

### Frontend (Svelte)

```json
{
  "dependencies": {
    "svelte": "^4.0.0",
    "vite": "^5.0.0",
    "axios": "^1.6.0",
    "marked": "^11.0.0",
    "tailwindcss": "^3.4.0"
  }
}
```

### Bases de Datos

| Tecnología | Uso | Tipo |
|-----------|-----|------|
| **PostgreSQL** | Usuarios, sesiones, auditoría | Relacional |
| **MongoDB** | Historial de conversaciones | Documental |
| **Qdrant** | Embeddings vectoriales (RAG) | Vectorial |
| **Redis** | Cache, rate limiting | En memoria |

### Infrastructure

- **Docker** + **Docker Compose**: Contenedorización
- **Kubernetes** (opcional): Orquestación y Network Policies
- **Nginx**: Reverse proxy y load balancing
- **Let's Encrypt**: Certificados SSL/TLS

---

## 📁 Estructura del Proyecto

```
weather-chatbot/
├── backend/                          # Backend Rust
│   ├── src/
│   │   ├── main.rs                   # Entry point
│   │   ├── config/                   # Configuration
│   │   ├── adapters/                 # Infrastructure adapters
│   │   │   ├── http/                 # REST API (Axum)
│   │   │   │   ├── routes/
│   │   │   │   ├── middleware/
│   │   │   │   └── handlers/
│   │   │   ├── repositories/         # Database implementations
│   │   │   │   ├── postgres.rs       # PostgreSQL adapter
│   │   │   │   ├── mongodb.rs        # MongoDB adapter
│   │   │   │   ├── qdrant.rs         # Qdrant adapter
│   │   │   │   └── redis.rs          # Redis adapter
│   │   │   └── external/             # External services
│   │   │       ├── llm_client.rs     # OpenAI/Claude client
│   │   │       └── dataframe.rs      # CONAGUA data loader
│   │   ├── application/              # Use cases (ports)
│   │   │   ├── services/
│   │   │   │   ├── auth_service.rs
│   │   │   │   ├── chat_orchestrator.rs
│   │   │   │   └── session_manager.rs
│   │   │   └── ports/                # Interface definitions
│   │   │       ├── user_repository.rs
│   │   │       ├── chat_repository.rs
│   │   │       └── llm_provider.rs
│   │   ├── domain/                   # Core business logic
│   │   │   ├── entities/
│   │   │   │   ├── user.rs
│   │   │   │   ├── session.rs
│   │   │   │   ├── message.rs
│   │   │   │   └── weather_data.rs
│   │   │   ├── services/
│   │   │   │   ├── intent_parser.rs
│   │   │   │   ├── rag_service.rs
│   │   │   │   ├── llm_service.rs
│   │   │   │   └── weather_query.rs
│   │   │   └── value_objects/
│   │   └── infrastructure/           # Cross-cutting concerns
│   │       ├── logging.rs
│   │       ├── metrics.rs
│   │       └── error.rs
│   ├── tests/
│   │   ├── integration/
│   │   └── unit/
│   ├── Cargo.toml
│   └── Dockerfile
├── frontend/                         # Frontend Svelte
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   ├── Chat.svelte
│   │   │   │   ├── MessageList.svelte
│   │   │   │   └── InputBox.svelte
│   │   │   └── stores/
│   │   │       └── auth.js
│   │   ├── routes/
│   │   │   ├── +page.svelte          # Home
│   │   │   └── chat/+page.svelte     # Chat interface
│   │   └── app.css
│   ├── static/
│   ├── package.json
│   └── Dockerfile
├── data/                             # Dataset CONAGUA
│   ├── raw/                          # CSV originales
│   └── processed/                    # Datos procesados
├── docs/                             # Documentación
│   ├── architecture/                 # Diagramas C4
│   │   ├── level1-context.png
│   │   ├── level2-containers.png
│   │   ├── level3-components.png
│   │   ├── data-view.png
│   │   └── security-view.png
│   ├── api/                          # API documentation
│   └── deployment/                   # Deployment guides
├── scripts/                          # Utility scripts
│   ├── setup_databases.sh
│   ├── generate_embeddings.py
│   └── load_conagua_data.py
├── docker-compose.yml                # Development environment
├── kubernetes/                       # K8s manifests
│   ├── deployments/
│   ├── services/
│   └── network-policies/             # Microsegmentation
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Instalación y Configuración

### Prerequisitos

- **Rust** 1.75+ ([rustup](https://rustup.rs/))
- **Node.js** 18+ ([nvm](https://github.com/nvm-sh/nvm))
- **Docker** 24+ & **Docker Compose** 2.0+
- **PostgreSQL** 15+
- **MongoDB** 6+
- **Redis** 7+
- **Qdrant** 1.7+

### Instalación Rápida con Docker Compose

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/weather-chatbot.git
cd weather-chatbot

# 2. Copiar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 3. Iniciar servicios
docker-compose up -d

# 4. Verificar que todo esté corriendo
docker-compose ps

# 5. Cargar dataset CONAGUA
python scripts/load_conagua_data.py --source data/raw/conagua.csv

# 6. Generar embeddings para RAG
python scripts/generate_embeddings.py

# 7. Acceder a la aplicación
# Frontend: http://localhost:3000
# API: http://localhost:8080
# API Docs: http://localhost:8080/api/docs
```

### Instalación Manual (Desarrollo)

#### Backend (Rust)

```bash
cd backend

# Instalar dependencias
cargo build

# Ejecutar migraciones
sqlx migrate run

# Ejecutar tests
cargo test

# Iniciar servidor de desarrollo
cargo run

# Servidor corriendo en http://localhost:8080
```

#### Frontend (Svelte)

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev

# Aplicación corriendo en http://localhost:3000

# Build para producción
npm run build
```

### Configuración de Variables de Entorno

```bash
# .env
# Database URLs
DATABASE_URL=postgresql://user:password@localhost:5432/weather_chatbot
MONGODB_URL=mongodb://localhost:27017/weather_chatbot
REDIS_URL=redis://localhost:6379
QDRANT_URL=http://localhost:6333

# LLM Provider
LLM_PROVIDER=openai  # o 'anthropic', 'local'
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# JWT Secret (genera uno seguro)
JWT_SECRET=your-super-secret-key-change-this
JWT_EXPIRATION=3600  # segundos

# Server
PORT=8080
HOST=0.0.0.0
RUST_LOG=info

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60  # segundos
```

---

## 💻 Uso

### API Endpoints

#### Autenticación

```bash
# Registro de usuario
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "securepassword123"
}

# Login
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "securepassword123"
}
# Response: { "access_token": "eyJ...", "refresh_token": "..." }

# Refresh token
POST /api/auth/refresh
{
  "refresh_token": "..."
}
```

#### Chat

```bash
# Enviar mensaje (REST)
POST /api/chat/message
Authorization: Bearer <token>
{
  "message": "¿Cuál fue la temperatura máxima en Culiacán la semana pasada?",
  "session_id": "optional-uuid"
}

# WebSocket (streaming)
WS /api/chat/stream
Authorization: Bearer <token>
{
  "message": "¿Cuánta lluvia cayó en Sinaloa en enero?",
  "session_id": "optional-uuid"
}
```

#### Historial

```bash
# Obtener historial de conversación
GET /api/chat/history/:session_id
Authorization: Bearer <token>

# Listar sesiones del usuario
GET /api/chat/sessions
Authorization: Bearer <token>
```

### Ejemplos de Consultas

```
Usuario: "¿Cuál fue la temperatura promedio en Culiacán en diciembre de 2024?"
Bot: Según los datos de CONAGUA, la temperatura promedio en Culiacán durante 
     diciembre de 2024 fue de 24.5°C, con una máxima de 32°C y mínima de 18°C.

Usuario: "¿Llovió mucho en Sinaloa el mes pasado?"
Bot: En enero de 2025, Sinaloa registró una precipitación total de 45mm, 
     distribuida en 6 días. Esto está ligeramente por debajo del promedio 
     histórico de 52mm para este mes.

Usuario: "Dame un resumen del clima en Mazatlán esta semana"
Bot: Esta semana en Mazatlán:
     • Temperatura: 22-28°C
     • Humedad promedio: 68%
     • Viento: 15 km/h (brisa moderada)
     • Sin precipitaciones
     • Cielo mayormente despejado
```

---

## 🔒 Seguridad

### Controles Implementados

#### Capa de Red
- ✅ Firewall perimetral con IPS/IDS
- ✅ WAF (Web Application Firewall)
- ✅ DDoS protection
- ✅ TLS 1.3 obligatorio
- ✅ Geo-blocking opcional

#### Autenticación y Autorización
- ✅ JWT con RS256 (asimétrico)
- ✅ Bcrypt para passwords (cost factor 12)
- ✅ Refresh token rotation
- ✅ RBAC (Role-Based Access Control)
- ✅ Session timeout configurable
- ✅ MFA opcional (TOTP)

#### Protección de Aplicación
- ✅ Input sanitization
- ✅ SQL/NoSQL injection prevention
- ✅ XSS protection (CSP headers)
- ✅ CSRF tokens
- ✅ Rate limiting por usuario/IP
- ✅ Request size limits

#### Datos
- ✅ Encryption at rest (AES-256)
- ✅ Encryption in transit (TLS)
- ✅ Secrets management (Vault/AWS Secrets)
- ✅ Backup encryption
- ✅ Data masking en logs

#### Microsegmentación
- ✅ Network Policies (K8s) o Security Groups (AWS)
- ✅ Aislamiento por segmento
- ✅ Default Deny
- ✅ Least privilege access

### Auditoría y Compliance
- ✅ Logging estructurado (JSON)
- ✅ SIEM integration
- ✅ Alertas de seguridad
- ✅ Compliance: GDPR, SOC2
