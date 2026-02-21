\# TKT-01 — Explicación Metodológica Estructurada



\## 1. Información General



| Campo | Descripción |

|-------|------------|

| Template ID | TKT-01 |

| Nombre | Explicación Metodológica Estructurada |

| Categoría | Transferencia de Conocimiento |

| Relacionado con | P-01 a P-20 |

| Dominio | Datos hidrometeorológicos CONAGUA |

| Objetivo | Explicar de forma estructurada un análisis estadístico previamente realizado |



---



\## 2. Objetivo del Template



Este template permite que un modelo de lenguaje explique de manera clara, reproducible y técnicamente estructurada un análisis estadístico previamente ejecutado dentro del dominio hidrometeorológico.



Se enfoca en:



\- Describir pasos metodológicos

\- Declarar supuestos estadísticos

\- Identificar limitaciones

\- Interpretar resultados

\- Evaluar posibilidad de generalización



---



\## 3. Estructura Formal del Prompt

Actúa como un especialista en análisis climatológico y metodología estadística.



Tu tarea es explicar detalladamente el análisis previamente realizado sobre \[DESCRIBIR ANALISIS].



Debes incluir obligatoriamente las siguientes secciones:



1\. Objetivo del análisis



2\. Variables utilizadas



3\. Procedimiento metodológico paso a paso



4\. Supuestos estadísticos involucrados



5\. Limitaciones del análisis



6\. Interpretación del resultado



7\. Posibilidad de generalización o aplicación a otro dataset



Reglas obligatorias:



\- No inventes información.



\- Usa únicamente los resultados proporcionados.



\- Si faltan datos, indícalo explícitamente.



\- Mantén un tono técnico pero claro.



Formato de salida:



\- Secciones numeradas



\- Texto estructurado



\- Conclusión final breve





---



\## 4. Guía de Estilo



\### Tono

Técnico-académico con claridad didáctica.



\### Nivel

Universitario (Ingeniería / Ciencia de Datos).



\### Estructura

Siempre numerada del 1 al 7.



\### Restricciones

\- No generar datos nuevos.

\- No modificar resultados originales.

\- No omitir supuestos estadísticos.

\- No realizar cálculos adicionales.



---



\## 5. Ejemplo de Ejecución



\### Entrada



Explica la regresión lineal anual realizada para la estación 25164 entre 1970 y 1980 donde se obtuvo una pendiente de +3.2 mm/año y un p-valor de 0.04.



\### Salida Esperada



1\. Objetivo del análisis  

Determinar si existe una tendencia significativa en la precipitación anual para la estación 25164 durante el periodo 1970–1980.



2\. Variables utilizadas  

\- Variable dependiente: Precipitación anual (mm)  

\- Variable independiente: Año  



3\. Procedimiento metodológico  

Se aplicó una regresión lineal simple donde la precipitación anual fue modelada como función lineal del tiempo.



4\. Supuestos estadísticos  

\- Linealidad  

\- Independencia de observaciones  

\- Homocedasticidad  

\- Normalidad de residuos  



5\. Limitaciones  

\- Periodo corto de análisis  

\- Posibles datos faltantes  

\- No se evaluó autocorrelación  



6\. Interpretación  

La pendiente positiva indica incremento promedio anual.  

El p-valor de 0.04 sugiere significancia estadística al nivel α = 0.05.



7\. Generalización  

La metodología puede aplicarse a otras estaciones con series anuales completas.



Conclusión:  

Existe evidencia estadística de tendencia creciente en el periodo analizado.



---



\## 6. Validación



| Criterio | Cumple |

|----------|--------|

| Explica pasos metodológicos | ✔ |

| Declara supuestos | ✔ |

| Expone limitaciones | ✔ |

| Permite transferencia a otro dataset | ✔ |

| Coherente con US-2.1 | ✔ |



---





