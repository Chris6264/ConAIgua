# TKT-10 — Marco de Toma de Decisiones Basado en Evidencia Estadística

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-10 |
| Nombre | Marco de Toma de Decisiones Basado en Evidencia |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-01 a P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Traducir resultados estadísticos en recomendaciones estructuradas para toma de decisiones |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje:

- Interprete resultados estadísticos en contexto aplicado.
- Identifique implicaciones prácticas.
- Diferencie evidencia fuerte de evidencia débil.
- Incorpore incertidumbre en recomendaciones.
- Construya decisiones fundamentadas sin extrapolación indebida.

Su propósito es conectar análisis cuantitativo con acción informada.

---

## 3. Estructura Formal del Prompt
Actúa como un especialista en análisis estadístico aplicado y toma de decisiones basada en evidencia.

Tu tarea es transformar el siguiente resultado analítico en un marco estructurado de toma de decisiones:

[DESCRIBIR RESULTADO O ANALISIS]

Debes incluir obligatoriamente:

1. Resumen del resultado estadístico

2. Nivel de evidencia (fuerte, moderada, débil)

3. Implicaciones prácticas directas

4. Riesgos asociados a la decisión

5. Impacto de la incertidumbre

6. Escenarios posibles (conservador, intermedio, optimista)

7. Recomendación final fundamentada

Reglas obligatorias:

- No convertir correlación en causalidad.

- No extrapolar fuera del periodo o datos analizados.

- Incorporar explícitamente incertidumbre.

- No emitir recomendaciones absolutas si la evidencia es limitada.

Formato de salida:

- Secciones numeradas

- Lenguaje técnico claro

- Recomendación estructurada

---

## 4. Guía de Estilo

### Tono
Estratégico-técnico, orientado a decisión responsable.

### Nivel
Avanzado (Ciencia de Datos Aplicada / Gestión basada en evidencia).

### Estructura
Numerada del 1 al 7 obligatoriamente.

### Restricciones
- No exagerar impacto.
- No asumir causalidad.
- No omitir limitaciones.

---

## 5. Ejemplo de Ejecución

### Entrada

Transforma en marco de decisión una regresión que muestra incremento de 3.2 mm/año en precipitación (p = 0.04).

### Salida Esperada

1. Resumen  
Se observa tendencia creciente significativa en precipitación anual.

2. Nivel de evidencia  
Evidencia moderada (p < 0.05, pero periodo corto).

3. Implicaciones  
Posible incremento gradual de precipitación en el periodo analizado.

4. Riesgos  
Sobreinterpretación temporal y falta de validación en periodos más amplios.

5. Incertidumbre  
Intervalo amplio sugiere variabilidad considerable.

6. Escenarios  
- Conservador: la tendencia podría estabilizarse.  
- Intermedio: incremento moderado sostenido.  
- Optimista: aumento continuo.  

7. Recomendación  
Ampliar análisis a periodos mayores antes de implementar decisiones estructurales.

---

## 6. Validación

| Criterio | Cumple |
|----------|--------|
| Traduce análisis en decisión | ✔ |
| Incorpora incertidumbre | ✔ |
| No exagera resultados | ✔ |
| Diferencia evidencia fuerte/débil | ✔ |
| Coherente con US-2.1 | ✔ |

---
