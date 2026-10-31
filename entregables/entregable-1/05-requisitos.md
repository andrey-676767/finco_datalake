# 5. Matriz de requisitos funcionales y no funcionales

**Versión:** 1.1 — 25 de octubre de 2026
**Fuente de los IDs y descripciones breves:** matriz de trazabilidad del README (§11). Las descripciones completas, los criterios de verificación y las prioridades se redactaron para este documento a partir de las historias de usuario y los casos de prueba del README.

> **Importante.** El README indica que los requisitos completos están en la sección 13 del documento base, que no está en el repositorio. Hay que contrastar esta matriz con ese documento antes de entregar.

**Convenciones**

- **Prioridad (MoSCoW):** Must = necesaria para el MVP · Should = importante, puede reducirse · Could = deseable. Se deriva de la prioridad de las HU enlazadas (Alta → Must, Media → Should). Donde no hay HU asociada, es una propuesta.
- **Fuente:** técnica de elicitación de origen, según `04-elicitacion.md` (T1 análisis documental, T2 decisiones del equipo, T3 prueba técnica, T4 entrevista al profesor, T5 encuesta).
- **Estado:** todos los requisitos están `Pendiente` de implementación según el README v1.0.

---

## 1. Requisitos funcionales (RF)

| ID | Requisito | Descripción | Prioridad | Fuente | Criterio de verificación | HU | Caso de prueba |
|---|---|---|---|---|---|---|---|
| RF-01 | Extracción de fuentes | El sistema debe extraer la TRM (API Socrata de datos.gov.co), el IPC y la tasa de intervención (Banco de la República) desde el 1 de enero de 2020, con reintentos y registro de errores ante fallas de red. | Must | T1, T2 (D-01, D-02) | El extractor recorre todas las páginas de la API y, ante fallas, reintenta al menos 3 veces y termina con código distinto de 0 | HU-03, 04, 05, 06 | CP-ING-01, CP-ING-02 |
| RF-01b | Conciliación de periodicidades | El sistema debe resolver la periodicidad mixta (diaria, mensual y por vigencia) con la Opción B: hechos separados, tasa modelada con `fecha_inicio` y `fecha_fin`, y un mart mensual en gold. | Must | T2 (D-03) | Las vigencias de la tasa no se solapan y el mart tiene una fila por mes desde 2020 | HU-08, 09 | CP-SIL-02, CP-GLD-02 |
| RF-02 | Conservación de datos crudos | El sistema debe guardar en bronze el dato original sin transformar, como archivo Parquet inmutable por lote (replicado en PostgreSQL), con metadatos de fuente, fecha y hora de carga e identificador de lote. | Must | T1, T2 (D-04) | Todo registro bronze tiene los tres metadatos | HU-03, 04, 05 | CP-ING-03 |
| RF-03 | Limpieza y tipado | El sistema debe limpiar, tipar y deduplicar los datos en silver. | Must | T1, T2 (D-04) | Silver tiene un registro por fecha (TRM) y por mes (IPC) | HU-07, 08 | CP-SIL-01 |
| RF-04 | Esquema estrella | El sistema debe modelar en gold una dimensión de fecha, un hecho diario de TRM, un hecho mensual de indicadores y un mart mensual. | Must | T1, T2 (D-03) | Existen las tablas y el mart consolida TRM promedio, IPC y tasa vigente por mes | HU-09 | CP-GLD-02 |
| RF-05 | Calidad automática | El sistema debe ejecutar pruebas automáticas de calidad: unicidad, no nulidad, integridad referencial y rangos válidos. | Must | T1 | `dbt build` y `dbt test` pasan sin fallas | HU-07, 08, 10 | CP-SIL-01, CP-GLD-01 |
| RF-06 | Linaje y documentación de datos | El sistema debe permitir consultar de qué fuente y transformación sale cada campo, con descripción de columnas. | Should | T1 | `dbt docs` muestra el grafo desde bronze hasta el mart y cada columna del mart tiene descripción | HU-11 | Aceptación de HU-11 |
| RF-07 | Tablero analítico | El sistema debe ofrecer un tablero con al menos 3 visualizaciones (evolución de la TRM, inflación anual y tasa de intervención frente a inflación) y filtro por rango de fechas. | Must | T1, T5 (por validar) | El tablero muestra 3 visualizaciones con datos y el filtro funciona | HU-13 | CP-DASH-01 |
| RF-08 | Ejecución con un solo comando | El sistema debe ejecutar ingesta y `dbt build` en orden con un solo comando (`docker compose run --rm pipeline`), informar la duración y terminar con código 0 si todo fue exitoso. | Must | T2 (D-05) | El comando termina con código 0 y reporta la duración | HU-12, 02 | CP-E2E-01 |
| RF-09 | Aplicación web de consulta y extracción | El sistema debe ofrecer una aplicación web, aparte del tablero, que permita visualizar los datos de gold (TRM diaria, indicadores mensuales y mart mensual), filtrarlos por rango de fechas y descargarlos en CSV. | Should | Petición del PO (25 oct) | La aplicación muestra los datos y el archivo descargado contiene solo el rango y el conjunto elegidos | HU-14 | CP-APP-01 |

## 2. Requisitos no funcionales (RNF)

| ID | Categoría | Descripción | Prioridad | Fuente | Criterio de verificación | HU | Caso de prueba |
|---|---|---|---|---|---|---|---|
| RNF-01 | Portabilidad / reproducibilidad | El entorno completo (PostgreSQL, Metabase, pipeline y aplicación web) debe levantarse con Docker Compose en una máquina limpia que solo tenga Docker, siguiendo solo el README. El tablero queda ya cargado con datos. | Must | T2 (D-04, D-05) | `docker compose up -d` crea los esquemas y Metabase responde | HU-01, 02 | CP-INST-01 |
| RNF-02 | Rendimiento | El pipeline completo debe ejecutarse en menos de **5 minutos** (umbral provisional, sin contar la descarga de imágenes Docker). Se revisa tras medir: umbral final = el doble de lo medido. | Must (umbral por definir) | Sin definir. Validar en T4 | Medición de duración en `pipeline.py` frente al umbral | HU-12 | Medición de rendimiento |
| RNF-03 | Mantenibilidad / estilo | El código Python debe cumplir PEP 8 (verificado con `ruff`). El estilo de SQL con `sqlfluff` es opcional. | Should (propuesta) | T2 (D-07) | `verificar.py` sin errores | Todas | `verificar.py` |
| RNF-04 | Mantenibilidad / versionado | Todo el código y las transformaciones deben estar versionados en Git. | Must (propuesta) | T2 (D-08) | Historial de Git con PR enlazados a HU | Todas | Historial Git |
| RNF-05 | Documentabilidad | La documentación de los modelos de datos debe generarse automáticamente con dbt. | Should | T1 | `dbt docs generate` y `dbt docs serve` funcionan | HU-11 | Aceptación de HU-11 |

> **RNF-02 provisional.** El umbral queda en 5 minutos sin contar la descarga de imágenes Docker. Se revisa tras medir `pipeline` en el sprint 3: umbral final = el doble de lo medido.

## 3. Restricciones

| ID | Restricción | Origen |
|---|---|---|
| R-01 | No hay integración continua. Las pruebas se ejecutan localmente antes de cada PR y se pega el resultado en el PR | D-07 |
| R-02 | El evaluador debe poder ejecutar todo el proyecto en su propia máquina | D-05 |
| R-03 | El histórico comienza en enero de 2020 | D-02 |
| R-04 | Dedicación de aproximadamente 5 horas por semana por integrante | Plan de proyecto |
| R-05 | Tecnologías fijadas: PostgreSQL, dbt Core, Python, Metabase y Docker | D-04 |
| R-06 | Fuentes de datos públicas y gratuitas | Alcance del proyecto |

## 4. Matriz requisito × historia de usuario

Marca cada HU que implementa o verifica un requisito.

| Requisito | HU-01 | HU-02 | HU-03 | HU-04 | HU-05 | HU-06 | HU-07 | HU-08 | HU-09 | HU-10 | HU-11 | HU-12 | HU-13 | HU-14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RF-01 | | | ● | ● | ● | ● | | | | | | | | |
| RF-01b | | | | | | | | ● | ● | | | | | |
| RF-02 | | | ● | ● | ● | | | | | | | | | |
| RF-03 | | | | | | | ● | ● | | | | | | |
| RF-04 | | | | | | | | | ● | | | | | |
| RF-05 | | | | | | | ● | ● | | ● | | | | |
| RF-06 | | | | | | | | | | | ● | | | |
| RF-07 | | | | | | | | | | | | | ● | |
| RF-08 | | ● | | | | | | | | | | ● | | |
| RF-09 | | | | | | | | | | | | | | ● |
| RNF-01 | ● | ● | | | | | | | | | | | | |
| RNF-02 | | | | | | | | | | | | ● | | |
| RNF-05 | | | | | | | | | | | ● | | | |

RNF-03 y RNF-04 aplican a todas las historias.

## 5. Verificación de cobertura

| Verificación | Resultado |
|---|---|
| ¿Todo RF tiene al menos una HU? | Sí (RF-01 a RF-09 y RF-01b) |
| ¿Todo RNF tiene al menos una HU o mecanismo de verificación? | Sí. RNF-03 se verifica con `verificar.py` y RNF-04 con el historial de Git |
| ¿Toda HU enlaza al menos un requisito? | Sí (ver `06-product-backlog.md`) |
| ¿Todo requisito tiene un criterio verificable? | Todos. RNF-02 con umbral provisional (menos de 5 minutos), a revisar tras medir |
