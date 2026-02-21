# TKT-02 — Reinterpretación Metodológica en Nuevo Dataset

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-02 |
| Nombre | Reinterpretación Metodológica en Nuevo Dataset |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-01 a P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Reinterpretar un análisis previo aplicándolo conceptualmente a un nuevo dataset |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje:

- Tome un análisis estadístico previamente realizado.
- Lo adapte conceptualmente a un nuevo dataset.
- Identifique posibles cambios en resultados.
- Evalúe diferencias estructurales entre datasets.
- Explique implicaciones metodológicas.

El objetivo es transferir conocimiento analítico entre estaciones, periodos o regiones.

---

## 3. Estructura Formal del Prompt
Actúa como un especialista en análisis climatológico comparativo.

Tu tarea es reinterpretar el análisis previamente realizado sobre [DESCRIBIR ANALISIS ORIGINAL] aplicándolo conceptualmente al nuevo dataset [DESCRIBIR NUEVO DATASET].

Debes incluir obligatoriamente las siguientes secciones:

1. Resumen del análisis original

2. Descripción del nuevo dataset

3. Comparación estructural entre datasets

4. Ajustes metodológicos necesarios (si aplica)

5. Posibles cambios esperados en resultados

6. Limitaciones de la reinterpretación

7. Conclusión comparativa

Reglas obligatorias:

- No inventes datos del nuevo dataset.

- Si no se proporcionan resultados nuevos, indicar que el análisis es hipotético.

- Mantener coherencia metodológica con el análisis original.

- No realizar cálculos adicionales si no se proporcionan datos.

Formato de salida:

- Secciones numeradas

- Comparaciones explícitas

- Conclusión final estructurada


---

## 4. Guía de Estilo

### Tono
Técnico-comparativo, orientado a análisis científico.

### Nivel
Universitario / Ingeniería / Ciencia de Datos.

### Estructura
Numerada del 1 al 7 obligatoriamente.

### Restricciones
- No generar valores numéricos nuevos.
- No asumir comportamientos climáticos sin evidencia.
- Declarar explícitamente cuando la reinterpretación es conceptual.

---

## 5. Ejemplo de Ejecución

### Entrada

Reinterpreta la regresión anual realizada para la estación 25164 (1970–1980) aplicándola a la estación 25034 en el mismo periodo.

### Salida Esperada

1. Resumen del análisis original  
Se aplicó una regresión lineal simple para evaluar tendencia anual de precipitación.

2. Descripción del nuevo dataset  
La estación 25034 pertenece al mismo estado pero presenta condiciones climáticas costeras distintas.

3. Comparación estructural  
Ambas estaciones poseen registros anuales completos, pero su ubicación geográfica difiere significativamente.

4. Ajustes metodológicos  
Podría requerirse evaluación adicional de estacionalidad si el régimen de lluvias es distinto.

5. Cambios esperados  
La pendiente podría diferir debido a diferencias microclimáticas.

6. Limitaciones  
No se proporcionaron datos numéricos del segundo análisis.

7. Conclusión comparativa  
La metodología es transferible, pero los resultados deben validarse empíricamente.

---

## 6. Validación

| Criterio | Cumple |
|----------|--------|
| Permite reinterpretación | ✔ |
| Explica ajustes metodológicos | ✔ |
| Declara limitaciones | ✔ |
| Evita invención de datos | ✔ |
| Coherente con US-2.1 | ✔ |
