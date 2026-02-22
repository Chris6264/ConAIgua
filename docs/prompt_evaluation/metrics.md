# Marco de Métricas para Evaluación de Calidad de Prompts

## 1. Objetivo

Definir métricas objetivas y reproducibles para evaluar la calidad de los prompts utilizados por agentes inteligentes en el dominio hidrometeorológico, asegurando coherencia, precisión y estabilidad en las respuestas generadas.

---

## 2. Métricas Definidas

### 2.1 Coherencia

#### Definición Formal
Grado en el que la respuesta generada mantiene consistencia lógica, estructural y semántica respecto a la instrucción original.

#### Indicadores
- Cumplimiento de estructura solicitada.
- Orden lógico de secciones.
- Ausencia de contradicciones internas.
- Claridad en la organización del contenido.

#### Escala (0–5)

| Puntaje | Descripción |
|----------|-------------|
| 0 | Respuesta incoherente |
| 1 | Múltiples contradicciones |
| 2 | Estructura parcial |
| 3 | Coherencia moderada |
| 4 | Estructura correcta con leves fallas |
| 5 | Totalmente coherente y estructurada |

#### Umbral mínimo aceptable
≥ 4

---

### 2.2 Precisión

#### Definición Formal
Grado en que la respuesta respeta estrictamente los datos, reglas y restricciones establecidas en el prompt.

#### Indicadores
- No inventa datos.
- Respeta variables permitidas.
- Cumple proceso obligatorio.
- Exactitud técnica y estadística.

#### Escala (0–5)

| Puntaje | Descripción |
|----------|-------------|
| 0 | Invención evidente de datos |
| 1 | Múltiples errores técnicos |
| 2 | Errores relevantes |
| 3 | Precisión moderada |
| 4 | Leves imprecisiones menores |
| 5 | Exactitud total |

#### Umbral mínimo aceptable
≥ 4.5

---

### 2.3 Estabilidad

#### Definición Formal
Consistencia de la salida ante ejecuciones repetidas del mismo prompt bajo las mismas condiciones.

#### Procedimiento de medición
- Ejecutar el mismo prompt N veces (mínimo 10).
- Medir similitud semántica promedio.
- Analizar variaciones estructurales.

#### Escala (0–5)

| Puntaje | Descripción |
|----------|-------------|
| 0 | Alta variabilidad |
| 2 | Variaciones significativas |
| 3 | Variaciones moderadas |
| 4 | Variaciones leves |
| 5 | Respuestas prácticamente idénticas |

#### Umbral mínimo aceptable
≥ 4

---

## 3. Score Global

Score Global = (0.4 × Coherencia) + (0.4 × Precisión) + (0.2 × Estabilidad)

### Umbral Global
≥ 4.2 para aprobación.
