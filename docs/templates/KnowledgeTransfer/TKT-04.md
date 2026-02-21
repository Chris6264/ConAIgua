# TKT-04 — Evaluación Crítica de Supuestos Estadísticos

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-04 |
| Nombre | Evaluación Crítica de Supuestos Estadísticos |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-02, P-03, P-07, P-11, P-18, P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Analizar críticamente los supuestos estadísticos de un análisis previo y evaluar su impacto |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje examine rigurosamente los supuestos estadísticos involucrados en un análisis previamente realizado, evaluando:

- Qué supuestos se utilizaron
- Si dichos supuestos son razonables en el contexto climatológico
- Qué implicaciones tendría su incumplimiento
- Qué pruebas adicionales podrían realizarse
- Qué tan robustos son los resultados ante posibles violaciones

Se enfoca en fortalecer la validez metodológica del análisis.

---

## 3. Estructura Formal del Prompt
Actúa como un especialista en estadística aplicada y climatología.

Tu tarea es evaluar críticamente los supuestos estadísticos del siguiente análisis:

[DESCRIBIR ANALISIS TECNICO]

Debes incluir obligatoriamente las siguientes secciones:

1. Identificación de los supuestos estadísticos utilizados

2. Explicación técnica de cada supuesto

3. Evaluación de plausibilidad en el contexto hidrometeorológico

4. Consecuencias de la violación de cada supuesto

5. Métodos alternativos si los supuestos no se cumplen

6. Impacto potencial en la interpretación de resultados

7. Conclusión sobre la robustez del análisis

Reglas obligatorias:

- No inventar resultados adicionales.

- Basarse únicamente en la metodología descrita.

- Si no se proporcionan datos suficientes, indicarlo explícitamente.

- Mantener rigor técnico.

Formato de salida:

- Secciones numeradas

- Explicaciones técnicas claras

- Conclusión estructurada


---

## 4. Guía de Estilo

### Tono
Técnico-avanzado, orientado a revisión metodológica.

### Nivel
Avanzado (Estadística / Ciencia de Datos).

### Estructura
Numerada del 1 al 7 obligatoriamente.

### Restricciones
- No reinterpretar resultados numéricos.
- No generar pruebas estadísticas no solicitadas.
- No suavizar críticas metodológicas.

---

## 5. Ejemplo de Ejecución

### Entrada

Evalúa críticamente los supuestos de una regresión lineal anual aplicada a precipitación entre 1970 y 1980 en la estación 25164.

### Salida Esperada

1. Identificación de supuestos  
El modelo asume linealidad, independencia temporal, homocedasticidad y normalidad de residuos.

2. Explicación técnica  
La linealidad implica que el cambio en precipitación es constante por unidad de tiempo.  
La independencia implica ausencia de autocorrelación entre años consecutivos.

3. Evaluación en contexto climatológico  
En series climáticas anuales puede existir autocorrelación debido a patrones multianuales (ENSO, variabilidad regional).

4. Consecuencias de violación  
Si existe autocorrelación, el p-valor podría estar subestimado.

5. Métodos alternativos  
Modelos ARIMA o regresión con corrección de autocorrelación.

6. Impacto en interpretación  
La significancia estadística podría reducirse si los supuestos no se cumplen.

7. Conclusión  
El análisis es metodológicamente válido bajo los supuestos clásicos, pero se recomienda verificar autocorrelación.

---

## 6. Validación

| Criterio | Cumple |
|----------|--------|
| Identifica supuestos | ✔ |
| Evalúa plausibilidad | ✔ |
| Explica consecuencias | ✔ |
| Propone alternativas | ✔ |
| Coherente con US-2.1 | ✔ |

---
