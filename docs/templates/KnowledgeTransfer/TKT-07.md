# TKT-07 — Integración y Síntesis de Resultados Múltiples

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-07 |
| Nombre | Integración y Síntesis de Resultados Múltiples |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-01 a P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Integrar múltiples análisis estadísticos en una conclusión estructurada y coherente |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje:

- Analice múltiples resultados estadísticos.
- Identifique relaciones entre ellos.
- Detecte coherencias o contradicciones.
- Construya una síntesis estructurada.
- Ofrezca una conclusión global fundamentada.

Su propósito es transformar análisis individuales en conocimiento integrado.

---

## 3. Estructura Formal del Prompt
Actúa como un especialista en análisis estadístico integrado y climatología.

Tu tarea es sintetizar e integrar los siguientes resultados analíticos:

[DESCRIBIR ANALISIS 1]
[DESCRIBIR ANALISIS 2]
[DESCRIBIR ANALISIS 3]
...

Debes incluir obligatoriamente:

1. Resumen breve de cada análisis

2. Identificación de relaciones entre resultados

3. Consistencias encontradas

4. Posibles contradicciones

5. Interpretación conjunta

6. Limitaciones globales

7. Conclusión integradora final

Reglas obligatorias:

- No inventar nuevos resultados.

- No resolver contradicciones sin evidencia.

- Declarar explícitamente incertidumbre si existe.

- Mantener coherencia con cada análisis individual.

Formato de salida:

- Secciones numeradas

- Síntesis estructurada

- Conclusión global clara


---

## 4. Guía de Estilo

### Tono
Analítico-integrador.

### Nivel
Avanzado (Ciencia de Datos / Investigación aplicada).

### Estructura
Numerada del 1 al 7 obligatoriamente.

### Restricciones
- No priorizar un análisis sin justificación.
- No generar hipótesis nuevas no sustentadas.
- No mezclar resultados incompatibles sin advertencia.

---

## 5. Ejemplo de Ejecución

### Entrada

Integra los siguientes resultados:

- Regresión anual (pendiente +3.2 mm/año, p = 0.04).
- Correlación entre TMAX y PRECIP (r = 0.45).
- Análisis de anomalías que muestra dos años extremos.

### Salida Esperada

1. Resumen  
La regresión muestra tendencia creciente; la correlación indica relación moderada entre temperatura y precipitación; las anomalías muestran variabilidad puntual.

2. Relaciones  
La tendencia creciente puede estar parcialmente asociada a cambios térmicos.

3. Consistencias  
Los análisis no presentan contradicciones directas.

4. Contradicciones  
No se observan inconsistencias metodológicas evidentes.

5. Interpretación conjunta  
Existe evidencia de incremento moderado de precipitación acompañado de relación parcial con temperatura.

6. Limitaciones  
Periodo corto y posible autocorrelación no evaluada.

7. Conclusión  
Los resultados sugieren un comportamiento creciente con variabilidad interanual significativa.

---

## 6. Validación

| Criterio | Cumple |
|----------|--------|
| Integra múltiples análisis | ✔ |
| Identifica coherencias y contradicciones | ✔ |
| Mantiene rigor metodológico | ✔ |
| No inventa información | ✔ |
| Coherente con US-2.1 | ✔ |

---
