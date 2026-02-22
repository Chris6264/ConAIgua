# TKT-09 — Evaluación de Incertidumbre y Análisis de Sensibilidad

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-09 |
| Nombre | Evaluación de Incertidumbre y Sensibilidad |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-07, P-11, P-18, P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Evaluar la incertidumbre estadística y la sensibilidad de un modelo o análisis |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje:

- Analice el nivel de incertidumbre asociado a un resultado.
- Interprete intervalos de confianza y errores estándar.
- Evalúe estabilidad del modelo ante variaciones en datos.
- Determine la robustez del análisis.
- Identifique riesgos derivados de alta variabilidad.

Se enfoca en fortalecer la interpretación probabilística y evitar conclusiones deterministas.

---

## 3. Estructura Formal del Prompt
Actúa como un especialista en estadística inferencial y análisis de sensibilidad.

Tu tarea es evaluar la incertidumbre y la sensibilidad del siguiente resultado:

[DESCRIBIR MODELO O RESULTADO]

Debes incluir obligatoriamente:

1. Identificación de métricas de incertidumbre reportadas

2. Interpretación técnica de dichas métricas

3. Evaluación del nivel de incertidumbre

4. Análisis de sensibilidad ante posibles variaciones en datos

5. Riesgos asociados a alta variabilidad

6. Impacto en la interpretación final

7. Conclusión sobre robustez del resultado

Reglas obligatorias:

- No generar intervalos no proporcionados.

- No asumir precisión absoluta.

- Declarar explícitamente el nivel de confianza si se menciona.

- Mantener rigor técnico.

Formato de salida:

- Secciones numeradas

- Explicación técnica clara

- Conclusión estructurada


---

## 4. Guía de Estilo

### Tono
Inferencial y técnico.

### Nivel
Avanzado (Estadística Aplicada / Ciencia de Datos).

### Estructura
Numerada del 1 al 7 obligatoriamente.

### Restricciones
- No reinterpretar métricas.
- No suavizar incertidumbre.
- No omitir advertencias cuando el intervalo sea amplio.

---

## 5. Ejemplo de Ejecución

### Entrada

Evalúa la incertidumbre de una regresión donde la pendiente es 3.2 mm/año con intervalo de confianza 95% [0.5, 5.9] y p = 0.04.

### Salida Esperada

1. Métricas reportadas  
Se reporta intervalo de confianza al 95% y p-valor.

2. Interpretación  
El intervalo indica que la pendiente verdadera se encuentra entre 0.5 y 5.9 mm/año con 95% de confianza.

3. Nivel de incertidumbre  
El intervalo es relativamente amplio, lo que sugiere variabilidad considerable.

4. Sensibilidad  
Si el intervalo incluyera valores cercanos a cero, la significancia podría verse comprometida.

5. Riesgos  
Sobreinterpretar la magnitud exacta del incremento.

6. Impacto  
Aunque el resultado es significativo, la magnitud precisa es incierta.

7. Conclusión  
El modelo muestra tendencia positiva, pero con incertidumbre moderada en la estimación puntual.

---

## 6. Validación

| Criterio | Cumple |
|----------|--------|
| Interpreta incertidumbre | ✔ |
| Evalúa sensibilidad | ✔ |
| No inventa métricas | ✔ |
| Mantiene rigor inferencial | ✔ |
| Coherente con US-2.1 | ✔ |

---
