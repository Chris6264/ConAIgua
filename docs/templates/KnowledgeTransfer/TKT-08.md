# TKT-08 — Comparación Crítica entre Modelos Estadísticos

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-08 |
| Nombre | Comparación Crítica entre Modelos Estadísticos |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-07, P-11, P-18, P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Comparar críticamente dos o más modelos estadísticos y evaluar su adecuación |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje:

- Compare metodológicamente dos o más modelos.
- Analice diferencias en supuestos.
- Evalúe métricas de desempeño (R², MAE, RMSE, etc.).
- Determine fortalezas y debilidades.
- Recomiende el modelo más adecuado según contexto.

Se enfoca en selección informada de modelos.

---

## 3. Estructura Formal del Prompt
# TKT-08 — Comparación Crítica entre Modelos Estadísticos

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-08 |
| Nombre | Comparación Crítica entre Modelos Estadísticos |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-07, P-11, P-18, P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Comparar críticamente dos o más modelos estadísticos y evaluar su adecuación |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje:

- Compare metodológicamente dos o más modelos.
- Analice diferencias en supuestos.
- Evalúe métricas de desempeño (R², MAE, RMSE, etc.).
- Determine fortalezas y debilidades.
- Recomiende el modelo más adecuado según contexto.

Se enfoca en selección informada de modelos.

---

## 3. Estructura Formal del Prompt
Actúa como un especialista en modelado estadístico y climatología.

Tu tarea es comparar críticamente los siguientes modelos:

[DESCRIBIR MODELO A]
[DESCRIBIR MODELO B]
[OPCIONAL: MODELO C]

Debes incluir obligatoriamente:

1. Descripción resumida de cada modelo

2. Diferencias metodológicas clave

3. Comparación de métricas de desempeño

4. Comparación de supuestos estadísticos

5. Ventajas y desventajas de cada modelo

6. Contextos donde cada modelo sería más apropiado

7. Recomendación final justificada

Reglas obligatorias:

- No inventar métricas no proporcionadas.

- No declarar superioridad sin justificación.

- Mantener coherencia con los resultados originales.

- Declarar incertidumbre si la comparación es incompleta.

Formato de salida:

- Secciones numeradas

- Comparación estructurada

- Recomendación final clara


---

## 4. Guía de Estilo

### Tono
Técnico-comparativo, orientado a toma de decisiones.

### Nivel
Avanzado (Ciencia de Datos / Modelado Estadístico).

### Estructura
Numerada del 1 al 7 obligatoriamente.

### Restricciones
- No reinterpretar resultados numéricos.
- No favorecer un modelo por preferencia teórica.
- No extrapolar más allá de los datos disponibles.

---

## 5. Ejemplo de Ejecución

### Entrada

Compara una regresión lineal simple (R² = 0.52) con una regresión múltiple (R² = 0.68) aplicada a precipitación anual.

### Salida Esperada

1. Descripción  
La regresión simple modela precipitación en función del tiempo.  
La múltiple incluye TMAX y TMIN como variables explicativas adicionales.

2. Diferencias metodológicas  
El modelo múltiple incorpora mayor complejidad y más variables predictoras.

3. Métricas  
El modelo múltiple presenta mayor R² (0.68 vs 0.52).

4. Supuestos  
Ambos comparten supuestos clásicos de linealidad y homocedasticidad.

5. Ventajas y desventajas  
La regresión simple es más interpretable; la múltiple tiene mayor capacidad explicativa.

6. Contexto  
La regresión múltiple es preferible cuando se desea explicación más detallada.

7. Recomendación  
El modelo múltiple ofrece mejor ajuste, pero debe evaluarse riesgo de sobreajuste.

---

## 6. Validación

| Criterio | Cumple |
|----------|--------|
| Compara modelos rigurosamente | ✔ |
| Evalúa métricas | ✔ |
| Analiza supuestos | ✔ |
| Proporciona recomendación justificada | ✔ |
| Coherente con US-2.1 | ✔ |

---
