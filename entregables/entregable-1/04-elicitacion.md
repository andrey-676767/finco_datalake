# 4. Informe de técnicas de elicitación

**Versión:** 1.1 — 25 de octubre de 2026
**Estado:** parcial. Las secciones 1 y 2 documentan lo que el repositorio evidencia. Las secciones 3 y 4 son instrumentos listos para aplicar, con los resultados **sin completar**.

> **Aviso de integridad.** Este informe no contiene resultados de entrevistas ni encuestas inventados. Las casillas marcadas `[POR COMPLETAR]` deben llenarse solo con información real. Si una técnica no se aplicó, hay que dejarlo escrito así en la entrega: un informe honesto con tres técnicas bien documentadas puntúa mejor que uno con cinco técnicas fabricadas.

---

## 1. Resumen de técnicas

| # | Técnica | Participantes | Estado | Evidencia |
|---|---|---|---|---|
| T1 | Análisis documental | Equipo | **Aplicada** | Documento base, README de planeación, páginas de las fuentes de datos |
| T2 | Sesiones de decisión del equipo (lluvia de ideas y consenso) | David, Juan Esteban, Andrey | **Aplicada** (según el registro de decisiones D-01 a D-08) | Tabla de decisiones del README (§1.1) |
| T3 | Prueba técnica de las fuentes (prototipado exploratorio) | David | **Aplicada (TRM); CSV del Banco confirmado como descarga manual** | Tarea de la semana 2: probar la API Socrata y confirmar el formato del Banco de la República (`docs/fuentes.md`) |
| T4 | Entrevista al evaluador (profesor) | Profesor | **Aplicada** (respuestas por escrito; fecha por completar) | Guía en la sección 3 |
| T5 | Encuesta o entrevista a usuarios del dominio (analista o estudiante de finanzas) | 3 a 5 personas | `[POR COMPLETAR]` | Instrumento en la sección 4 |

## 2. Técnicas aplicadas y hallazgos

### T1. Análisis documental

- **Objetivo.** Entender el dominio (indicadores, fuentes, periodicidades) y las expectativas de la entrega.
- **Fuentes revisadas.** Documento base del proyecto (`plan-proyecto-lakehouse-financiero.md`), README de planeación, datos.gov.co (TRM) y la sección de estadísticas del Banco de la República (IPC y tasa de intervención).
- **Hallazgos.**
  - Los tres indicadores tienen periodicidades distintas (diaria, mensual y por vigencia) y esto exige una regla de reconciliación → RF-01b.
  - La TRM se expone por API (Socrata) y el Banco de la República por archivos de descarga → RF-01 y HU-06 (reintentos y registro de errores).
  - La entrega exige un tablero, pruebas de calidad y trazabilidad → RF-05, RF-06 y RF-07.

### T2. Sesiones de decisión del equipo

- **Objetivo.** Acotar el alcance y las decisiones técnicas del MVP.
- **Participantes.** David Restrepo, Juan Esteban y Andrey Machado.
- **Resultados** (decisiones confirmadas):

| Decisión | Efecto sobre los requisitos |
|---|---|
| D-01 Indicadores: TRM, IPC y tasa de intervención | RF-01 |
| D-02 Histórico desde enero de 2020 | RF-01, HU-03 a HU-05 |
| D-03 Periodicidad mixta con Opción B | RF-01b, RF-04, HU-08, HU-09 |
| D-04 PostgreSQL, dbt Core, script Python y Metabase | RNF-01, RF-08 |
| D-05 El evaluador ejecuta todo en su máquina | RNF-01, RF-08, HU-02 |
| D-06 Cada integrante sustenta su parte | Roles y regla de aprobación |
| D-07 Sin integración continua | `verificar.py`, DoD |

- **Fecha(s) de las sesiones:** `[POR COMPLETAR]`

### T3. Prueba técnica de las fuentes

- **Objetivo.** Resolver incertidumbres que condicionan los requisitos: identificar el dataset de la TRM, la paginación, el filtro por fecha y el formato de descarga del IPC y la tasa de intervención.
- **Responsable.** David Restrepo.
- **Resultados esperados** (registrar en `docs/fuentes.md`):

| Pregunta | Respuesta |
|---|---|
| ¿Cuál es el identificador del dataset de la TRM en datos.gov.co? | `ceyp-9c7c` (Superfinanciera). Entrega `valor`, `vigenciadesde`, `vigenciahasta`; 8.374 filas en total |
| ¿La API pagina los resultados? ¿Con qué límite? | `[POR COMPLETAR]` |
| ¿Se puede filtrar desde 2020-01-01? | `[POR COMPLETAR]` |
| ¿En qué formato descarga el Banco de la República el IPC? (URL, formato, frecuencia) | CSV exportado a mano; sin URL directa |
| ¿En qué formato descarga la tasa de intervención? | CSV exportado a mano |
| ¿Es automatizable el formato del Banco de la República? | No por ahora. Mejora futura: URL directa o cambio de fuente |

## 3. Entrevista al evaluador (guía)

**Entrevistado:** profesor de la materia (stakeholder externo).
**Duración sugerida:** 15 a 20 minutos.
**Objetivo:** validar alcance, fechas y criterios de aceptación.

| # | Pregunta | Qué requisito valida |
|---|---|---|
| 1 | ¿Cuáles son las fechas exactas de la entrega de mitad y de la entrega final? | Cronograma |
| 2 | ¿Cómo va a ejecutar el proyecto? ¿Qué sistema operativo y qué software tendrá instalado (Docker, Python)? | RNF-01, RF-08, HU-02 |
| 3 | ¿Cuánto tiempo considera aceptable para que corra el pipeline completo? | RNF-02 (umbral "X minutos") |
| 4 | ¿Espera ver el tablero funcionando con datos ya cargados o que lo reconstruyamos desde cero? | HU-13, riesgo de Metabase |
| 5 | ¿Qué evidencia de pruebas espera (capturas, logs, reportes)? | Plan de pruebas |
| 6 | ¿Acepta que la integración continua quede fuera del alcance? | D-07 |
| 7 | ¿Qué documentos son obligatorios en cada entrega? | Entregables |
| 8 | ¿Hay algún indicador adicional o criterio que considere imprescindible? | Alcance |

**Registro de la entrevista**

| Campo | Valor |
|---|---|
| Fecha | `[POR COMPLETAR]` |
| Entrevistador | `[POR COMPLETAR]` |
| Respuestas y acuerdos | 1) Entorno: un Docker con todas las dependencias necesarias. 2) Entrega: un MVP con el repositorio y toda la documentación. 3) Tablero: ya cargado con datos. 4) Arquitectura: data warehouse, o el nombre más adecuado. 5) Habrá una revisión intermedia. 6) Acepta los CSV versionados en el repositorio. 7) No considera necesario ningún requisito adicional; el alcance le parece bien |
| Segunda ronda (respuestas por escrito) | a) Revisión intermedia el **30 de octubre de 2026**, que evalúa el **Entregable 2: Análisis, Diseño UML y Especificación Técnica** (casos de uso con plantilla, diagrama de actividades, diagrama de estado, diagrama de clases / modelo de dominio, arquitectura de alto nivel, diagramas de secuencia y de colaboración, plan preliminar de pruebas y estrategia de versionado). Criterios: sintaxis UML 35%, consistencia estático-dinámico-backlog 35%, pruebas derivadas de requisitos 20%, arquitectura 10%. Lo ideal es tener ya el MVP. b) Toda la documentación debe estar en el repositorio de GitHub, nada por fuera. c) El pipeline en menos de 5 minutos es aceptable. d) Sin comentarios sobre la aplicación web (HU-14) |
| Requisitos nuevos o modificados | RNF-01 y HU-02 (todo corre en Docker; el evaluador no instala Python), HU-13 (tablero entregado con datos), nombre "data warehouse" confirmado, D-07/alcance sin cambios |

## 4. Encuesta para usuarios del dominio (instrumento)

**Población objetivo.** Personas que consultan indicadores económicos: estudiantes de finanzas o economía, analistas, contadores.
**Muestra sugerida:** entre 5 y 10 respuestas (herramienta: Google Forms).
**Objetivo.** Priorizar visualizaciones y validar qué necesita el rol "analista financiero".

| # | Pregunta | Tipo de respuesta |
|---|---|---|
| 1 | ¿Con qué frecuencia consulta la TRM, el IPC o la tasa de intervención? | Diaria / Semanal / Mensual / Rara vez |
| 2 | ¿Dónde consulta hoy esos indicadores? | Respuesta abierta |
| 3 | ¿Cuál es la mayor dificultad al comparar esos indicadores? | Respuesta abierta |
| 4 | ¿Qué comparación le resulta más útil? | TRM vs. inflación / Tasa vs. inflación / TRM vs. tasa / Otra |
| 5 | ¿Qué rango de fechas suele analizar? | Último mes / Último año / Desde 2020 / Otro |
| 6 | ¿Qué tan importante es poder ver de qué fuente sale cada cifra? (1 a 5) | Escala |
| 7 | ¿Qué visualizaciones esperaría en el tablero? | Selección múltiple: línea de evolución, barras mensuales, comparativo entre indicadores, tabla |
| 8 | ¿Necesita exportar los datos? ¿En qué formato? | Sí / No + formato |

**Resultados**

| Pregunta | Resultado agregado |
|---|---|
| P1 a P8 | `[POR COMPLETAR]` |
| Número de participantes | `[POR COMPLETAR]` |

## 5. Trazabilidad entre elicitación y requisitos

La columna "Fuente" de `05-requisitos.md` indica la técnica de origen de cada requisito. La tabla siguiente resume el estado.

| Requisito | Origen verificable hoy | Validación pendiente |
|---|---|---|
| RF-01, RF-01b, RF-02 a RF-05 | T1 (documento base) y T2 (D-01 a D-04) | Contraste con la entrevista al profesor (T4) |
| RF-06, RF-07 | T1 (exigencias de la entrega) | Validar visualizaciones con la encuesta (T5) |
| RF-08, RNF-01 | T2 (D-05) | Confirmar el entorno del evaluador (T4, pregunta 2) |
| RNF-02 | Sin origen: el umbral no está definido | T4 (pregunta 3) y medición en el sprint 3 |
| RNF-03 a RNF-05 | T1 y T2 (D-04, D-07) | — |

## 6. Cómo cerrar este informe antes de la entrega

1. Confirmar con el equipo qué sesiones de decisión ocurrieron y en qué fechas (T2).
2. Completar los resultados de la prueba técnica de las fuentes con lo que David registre (T3).
3. Aplicar al menos la entrevista al profesor (T4). Es la técnica con mejor relación esfuerzo-valor, porque resuelve fechas, entorno de ejecución y el umbral de RNF-02.
4. Aplicar la encuesta (T5) si hay tiempo. Con 5 respuestas ya aporta evidencia para priorizar las visualizaciones.
5. Actualizar la columna "Fuente" de `05-requisitos.md` con lo que se haya obtenido.
