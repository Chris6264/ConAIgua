# TKT-03 — Traducción de Resultados Técnicos a Usuario No Experto

## 1. Información General

| Campo | Descripción |
|-------|------------|
| Template ID | TKT-03 |
| Nombre | Traducción Técnica a Usuario No Experto |
| Categoría | Transferencia de Conocimiento |
| Relacionado con | P-01 a P-20 |
| Dominio | Datos hidrometeorológicos CONAGUA |
| Objetivo | Explicar resultados estadísticos en lenguaje claro sin perder rigor conceptual |

---

## 2. Objetivo del Template

Este template permite que un modelo de lenguaje traduzca un análisis estadístico técnico a una explicación comprensible para usuarios no expertos, manteniendo:

- Precisión conceptual
- Claridad narrativa
- Contexto suficiente
- Advertencias sobre limitaciones

No simplifica en exceso ni elimina información crítica, sino que la comunica en términos accesibles.

---

## 3. Estructura Formal del Prompt
Actúa como un especialista en climatología con habilidades de divulgación científica.

Tu tarea es explicar los resultados del siguiente análisis técnico en un lenguaje claro y comprensible para una persona sin formación estadística:

[DESCRIBIR RESULTADO TECNICO]

Debes incluir obligatoriamente:

1. Explicación simple del objetivo del análisis

2. Qué significan los resultados en términos prácticos

3. Qué tan confiables son los resultados

4. Qué limitaciones existen

5. Qué implicaciones tiene para el usuario

Reglas obligatorias:

- No usar jerga técnica sin explicación.

- Si usas términos como "significancia", debes explicarlos.

- No inventar datos adicionales.

- Mantener coherencia con el análisis original.

Formato de salida:

- Párrafos claros

- Subtítulos breves

- Conclusión final sencilla


---

## 4. Guía de Estilo

### Tono
Claro, didáctico y accesible.

### Nivel
Persona sin formación técnica en estadística.

### Estructura
Explicación narrativa con subtítulos simples.

### Restricciones
- No eliminar advertencias metodológicas.
- No exagerar resultados.
- No interpretar más allá de los datos.

---

## 5. Ejemplo de Ejecución

### Entrada

Explica en términos simples que la regresión anual mostró una pendiente de +3.2 mm/año con p-valor de 0.04 para la estación 25164 entre 1970 y 1980.

### Salida Esperada

**¿Qué se estaba analizando?**  
Se evaluó si la cantidad de lluvia anual estaba aumentando o disminuyendo con el tiempo.

**¿Qué se encontró?**  
Los resultados indican que, en promedio, la lluvia aumentó aproximadamente 3.2 milímetros cada año durante el periodo analizado.

**¿Es confiable este resultado?**  
Sí, el análisis muestra que la probabilidad de que este aumento sea producto del azar es baja (menor al 5%), lo que sugiere que el incremento es estadísticamente significativo.

**¿Tiene limitaciones?**  
El análisis se realizó sobre un periodo relativamente corto (10 años), por lo que no necesariamente refleja tendencias de largo plazo.

**¿Qué significa en términos prácticos?**  
Durante esos años, la estación mostró una ligera tendencia a registrar más lluvia cada año.

**Conclusión:**  
Existe evidencia razonable de un aumento en la precipitación durante el periodo estudiado, aunque sería recomendable analizar un periodo más largo para confirmar la tendencia.

---

## 6. Validación

| Criterio | Cumple |
|----------|--------|
| Traduce resultados técnicos | ✔ |
| Mantiene coherencia estadística | ✔ |
| Explica confiabilidad | ✔ |
| Declara limitaciones | ✔ |
| Coherente con US-2.1 | ✔ |

---
