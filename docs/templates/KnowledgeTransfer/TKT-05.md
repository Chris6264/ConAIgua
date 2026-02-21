# TKT-05 — Análisis de Alcance, Riesgos y Responsabilidad de Interpretación

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-05 |
| Nombre | Análisis de Alcance y Riesgos de Interpretación |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-01 a P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Evaluar el alcance, límites y riesgos asociados a la interpretación de un análisis estadístico |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje:

- Analice el alcance real de un resultado estadístico.
- Identifique riesgos de sobreinterpretación.
- Declare explícitamente qué conclusiones son válidas y cuáles no.
- Diferencie correlación de causalidad.
- Establezca límites metodológicos y contextuales.

Su finalidad es evitar malas interpretaciones o uso indebido de resultados analíticos.

---

## 3. Estructura Formal del Prompt
Actúa como un especialista en estadística aplicada y análisis de riesgos interpretativos.

Tu tarea es evaluar el alcance y los posibles riesgos de interpretación del siguiente resultado analítico:

[DESCRIBIR RESULTADO O ANALISIS]

Debes incluir obligatoriamente las siguientes secciones:

1. Alcance real del resultado

2. Qué conclusiones son válidas

3. Qué conclusiones NO pueden afirmarse

4. Riesgos de sobreinterpretación

5. Diferenciación entre correlación y causalidad (si aplica)

6. Limitaciones contextuales (periodo, cobertura, datos faltantes)

7. Recomendaciones para uso responsable del resultado

Reglas obligatorias:

- No generar inferencias no respaldadas por el análisis.

- No convertir correlaciones en causalidades.

- No extrapolar fuera del periodo analizado.

- Declarar explícitamente incertidumbre cuando exista.

Formato de salida:

- Secciones numeradas

- Lenguaje técnico claro

- Conclusión estructurada sobre responsabilidad interpretativa


---

## 4. Guía de Estilo

### Tono
Técnico-crítico, orientado a evaluación responsable.

### Nivel
Avanzado (Ciencia de Datos / Investigación).

### Estructura
Numerada del 1 al 7 obligatoriamente.

### Restricciones
- No suavizar advertencias.
- No exagerar resultados.
- No asumir implicaciones políticas, económicas o climáticas no demostradas.

---

## 5. Ejemplo de Ejecución

### Entrada

Evalúa el alcance y riesgos interpretativos de una regresión que muestra aumento significativo de 3.2 mm/año en precipitación entre 1970 y 1980.

### Salida Esperada

1. Alcance real  
El resultado indica una tendencia creciente en precipitación únicamente dentro del periodo 1970–1980.

2. Conclusiones válidas  
Existe evidencia estadística de aumento promedio anual durante el periodo analizado.

3. Conclusiones no válidas  
No puede afirmarse que el clima global esté cambiando ni que la tendencia continúe después de 1980.

4. Riesgos de sobreinterpretación  
Extrapolar la tendencia a largo plazo sin datos adicionales.

5. Correlación vs causalidad  
El modelo describe asociación temporal, no identifica causas físicas.

6. Limitaciones contextuales  
Periodo corto y posible autocorrelación no evaluada.

7. Recomendaciones  
Ampliar análisis a periodos mayores y verificar estabilidad del modelo.

Conclusión:  
El resultado es estadísticamente válido en su contexto, pero su interpretación debe limitarse estrictamente al periodo y condiciones evaluadas.

---

## 6. Validación

| Criterio | Cumple |
|----------|--------|
| Define alcance del resultado | ✔ |
| Identifica riesgos de sobreinterpretación | ✔ |
| Diferencia correlación y causalidad | ✔ |
| Declara límites metodológicos | ✔ |
| Coherente con US-2.1 | ✔ |

---
