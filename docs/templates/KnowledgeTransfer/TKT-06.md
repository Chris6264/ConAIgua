# TKT-06 — Evaluación de Reproducibilidad y Trazabilidad Metodológica

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-06 |
| Nombre | Evaluación de Reproducibilidad y Trazabilidad |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-01 a P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Evaluar si un análisis estadístico puede ser reproducido y auditado correctamente |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje analice si un procedimiento estadístico previamente realizado:

- Es reproducible.
- Está completamente documentado.
- Tiene trazabilidad de datos.
- Puede ser auditado por terceros.
- Permite replicación con el mismo dataset.

Se enfoca en ciencia abierta, validación y rigor metodológico.

---

## 3. Estructura Formal del Prompt
Actúa como un especialista en reproducibilidad científica y auditoría estadística.

Tu tarea es evaluar la reproducibilidad y trazabilidad del siguiente análisis:

[DESCRIBIR ANALISIS]

Debes incluir obligatoriamente las siguientes secciones:

1. Claridad en la definición del dataset

2. Especificación de variables utilizadas

3. Descripción detallada del procedimiento

4. Transparencia en supuestos estadísticos

5. Información necesaria para replicar el análisis

6. Posibles ambigüedades o vacíos metodológicos

7. Conclusión sobre nivel de reproducibilidad

Reglas obligatorias:

- No agregar datos que no estén documentados.

- No asumir pasos metodológicos no descritos.

- Identificar explícitamente cualquier falta de información.

- Mantener evaluación técnica objetiva.

Formato de salida:

- Secciones numeradas

- Evaluación estructurada

- Conclusión clara sobre reproducibilidad (Alta, Media o Baja)


---

## 4. Guía de Estilo

### Tono
Técnico-objetivo, orientado a auditoría metodológica.

### Nivel
Avanzado (Investigación / Ciencia de Datos).

### Estructura
Numerada del 1 al 7 obligatoriamente.

### Restricciones
- No reinterpretar resultados.
- No validar calidad estadística (solo reproducibilidad).
- No suavizar ambigüedades detectadas.

---

## 5. Ejemplo de Ejecución

### Entrada

Evalúa la reproducibilidad de una regresión lineal anual aplicada a la estación 25164 entre 1970 y 1980 donde se reporta pendiente y p-valor.

### Salida Esperada

1. Claridad del dataset  
Se especifica estación y periodo, pero no se detallan criterios de exclusión de valores “Nulo”.

2. Variables utilizadas  
Se mencionan año y precipitación anual.

3. Procedimiento  
Se indica regresión lineal simple, pero no se especifica método de estimación.

4. Supuestos  
No se documenta verificación de normalidad ni autocorrelación.

5. Información para replicación  
Faltan detalles sobre tratamiento de datos faltantes.

6. Ambigüedades  
No se especifica nivel de significancia utilizado.

7. Conclusión  
Nivel de reproducibilidad: Medio.  
El análisis puede replicarse parcialmente, pero requiere mayor documentación.

---

## 6. Validación

| Criterio | Cumple |
|----------|--------|
| Evalúa trazabilidad | ✔ |
| Identifica vacíos metodológicos | ✔ |
| Clasifica reproducibilidad | ✔ |
| No inventa información | ✔ |
| Coherente con US-2.1 | ✔ |

---
