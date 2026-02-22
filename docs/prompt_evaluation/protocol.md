# Protocolo Reproducible de Evaluación de Prompts

## 1. Objetivo

Establecer un procedimiento estandarizado para evaluar la calidad de prompts de manera reproducible.

---

## 2. Procedimiento

1. Seleccionar prompt (ej: P-01).
2. Ejecutarlo 10 veces bajo mismas condiciones.
3. Guardar todas las salidas.
4. Aplicar evaluación automática:
   - Validación estructural.
   - Verificación de restricciones.
5. Aplicar evaluación humana técnica.
6. Registrar resultados en matriz.
7. Calcular Score Global.

---

## 3. Herramientas

- Script de estabilidad (similaridad semántica).
- Script validador de estructura.
- Hoja de matriz de evaluación versionada.
- Registro de versión de modelo y versión de prompt.

---

## 4. Reproducibilidad

Cada evaluación debe registrar:

- Fecha
- Versión del modelo
- Versión del prompt
- Parámetros de ejecución
- Número de iteraciones
