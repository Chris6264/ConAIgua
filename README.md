<div align="center">

# ConAIgua — Sistema de Consultas Hidrometeorológicas con LLM

![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)
![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow.svg)

[English Version](README.en.md)

</div>

Agente conversacional para consultar datos hidrometeorológicos históricos de CONAGUA (Comisión Nacional del Agua de México) mediante lenguaje natural, construido sobre LangGraph y un LLM servido por Groq (por defecto, puede ser cambiado por otro proveedor), con herramientas, prompts y reglas creadas a la medida para el dominio climatológico.

---

## Descripción general

**ConAIgua** permite consultar estadísticas, correlaciones, regresiones y tendencias sobre el dataset histórico de CONAGUA sin escribir código ni SQL. No es un modelo entrenado desde cero: usa un modelo base servido por Groq (por ejemplo `llama-3.3-70b-versatile`), al que el backend le agrega **herramientas propias, prompts, reglas de negocio y parámetros de generación** específicos para el análisis hidrometeorológico. 

### ¿Qué problema resuelve?

Los datos hidrometeorológicos históricos suelen estar en formatos poco accesibles (archivos `.txt` planos por estación, con metadatos y series diarias mezclados). ConAIgua permite:

- **Consultas en lenguaje natural**: "¿Cuál fue la temperatura máxima en la estación ALTO DE CULIACANCITO en enero de 1978?"
- **Análisis estadístico**: media, mediana, outliers, correlaciones (Pearson/Spearman), regresiones (simple/múltiple), tendencias anuales
- **Reportes automáticos**: generación de reportes EDA en HTML y Markdown por estación
- **Dominio especializado**: el agente entiende la estructura de estaciones CONAGUA, sus claves, estados y municipios

---

## Arquitectura de alto nivel

Estado actual: la interfaz web se comunica con un backend construido sobre LangGraph, que a su vez llama al LLM alojado en Groq. No hay bases de datos externas en uso todavía.

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
                        │   Configurado para       │
                        │   ConAIgua: herramientas,│
                        │   prompts y reglas       │
                        │   propias sobre datos    │
                        │   CONAGUA                │
                        └──────────────────────────┘
```

- **Frontend**: React + Next.js. Envía las consultas del usuario y muestra las respuestas del agente.
- **API Backend (LangGraph)**: orquesta el pipeline de datos, el motor EDA y la conversación; expone el agente al frontend vía HTTPS/WSS.
- **LLM (Groq)**: modelo base, no entrenado desde cero. Lo específico de ConAIgua es el conjunto de herramientas, prompts y reglas que el backend inyecta en cada llamada.

> **Roadmap (no implementado aún):** persistencia de usuarios/sesiones (PostgreSQL), historial de chat (MongoDB) y búsqueda semántica (Qdrant). Se documentarán aquí cuando se integren de verdad, no antes.

---

## Formato real del dataset CONAGUA

El dataset proviene de la **Base de Datos Climatológica Nacional** (CNA-SMN-CG-GMC-SMAA-CLIMATOLOGIA), con datos suministrados por las Oficinas Regionales de CONAGUA. Cada archivo de estación tiene el siguiente formato:

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

### Metadatos de estación

| Campo | Descripción | Ejemplo |
|---|---|---|
| `ESTACION` | Clave única de la estación | `25164` |
| `NOMBRE` | Nombre de la estación | `ALTO DE CULIACANCITO` |
| `ESTADO` | Estado de la República Mexicana | `SINALOA` |
| `MUNICIPIO` | Municipio de la estación | `CULIACAN` |
| `SITUACIÓN` | Estado operativo | `SUSPENDIDA` / `ACTIVA` |
| `ORGANISMO` | Organismo responsable | `CONAGUA-DGE` |
| `CVE-OMM` | Clave OMM internacional | `Nulo` o código numérico |
| `LATITUD` / `LONGITUD` | Coordenadas geográficas | `024.807°` / `-107.555°` |
| `ALTITUD` | Metros sobre el nivel del mar | `24 msnm` |
| `EMISION` | Fecha de emisión del reporte | `06/04/2020` |

### Registros diarios

| Campo | Descripción | Unidad |
|---|---|---|
| `FECHA` | Fecha de la observación | `DD/MM/YYYY` |
| `PRECIP` | Precipitación acumulada | mm |
| `EVAP` | Evaporación | mm |
| `TMAX` | Temperatura máxima del día | °C |
| `TMIN` | Temperatura mínima del día | °C |

---

## Pipeline de datos

```text
┌────────────┐   ┌──────────────┐   ┌──────────────────┐
│ TXT plano  │ → │  Pandas      │ → │  Parquet Store   │
│ CONAGUA    │   │  Transform   │   │  (dataset final) │
└────────────┘   └──────────────┘   └──────────────────┘
```

El pipeline (`run_data_pipeline`) parsea el formato propietario de CONAGUA, trata el literal `Nulo` como valor faltante, limpia el dataset y lo convierte a `data/processed/conAIgua_dataframe.parquet`, que es lo que consume el agente.

---

## Capacidades del agente

| Capacidad | Descripción |
|---|---|
| Estadísticas EDA | Media, mediana, min, max, std, outliers y estacionalidad |
| Correlaciones | Pearson y Spearman con p-value y significancia estadística |
| Regresiones | Lineal simple y múltiple con R², RMSE, IC 95% y diagnóstico |
| Tendencias | Análisis de tendencia anual en rangos de años |
| Reportes | HTML (ydata-profiling) y Markdown por estación |
| Estaciones | Listado de todas las estaciones disponibles |

---

## Stack tecnológico

| Área | Tecnología |
|---|---|
| Frontend | React 18, Next.js 14, pnpm, Docker |
| Backend / Agente | Python 3.12, LangChain, LangGraph |
| Datos | pandas, pyarrow (Parquet) |
| Estadística | scipy, scikit-learn |
| Reportes | ydata-profiling |
| Proveedores LLM soportados | Groq (por defecto), OpenAI, Anthropic, Google Gemini |

---

## Primeros pasos

El sistema se levanta en dos partes:

1. **Agente** — instalación, pipeline de datos y ejecución con LangGraph: [`conaigua-agent/README.md`](conaigua-agent/README.md)
2. **Interfaz web** — instalación de dependencias y ejecución con Docker: [`conaigua-chat-ui/README.md`](conaigua-chat-ui/README.md)

---

## Capturas de pantalla
 
**Vista general de la interfaz**
 
<img width="1850" height="657" alt="Vista general de la interfaz" src="https://github.com/user-attachments/assets/53e75300-5335-4ef6-b0b6-09c0947aaa9c" />

**Chat con el agente**
 
<img width="1852" height="926" alt="Chat con el agente" src="https://github.com/user-attachments/assets/9f72bbd2-8a70-4b27-9bc9-59ce24a056ae" />

**Pidiendo un reporte html al agente**
 
<img width="1416" height="653" alt="Reporte EDA en HTML" src="https://github.com/user-attachments/assets/dab65656-a471-4fe7-a939-cf0e90af32c5" />

**Reporte EDA en HTML**

<img width="1849" height="912" alt="Vista adicional" src="https://github.com/user-attachments/assets/115de2cd-9727-4476-a204-9a37934307ab" />
 
---

## Licencia

Copyright © 2026 Chris6264

Este proyecto está distribuido bajo la [Licencia Apache 2.0](LICENSE).
