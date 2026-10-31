# 1. Definición del problema y alcance del MVP

**Proyecto:** Lakehouse analítico de datos financieros públicos (`finco_datalake`)
**Materia:** Ingeniería de Software — Universidad Católica Luis Amigó
**Equipo:** David Restrepo (PO + ingesta) · Juan Esteban (modelos dbt) · Andrey Machado (Scrum Master, Docker / orquestación / Metabase)
**Versión:** 1.1 — 25 de octubre de 2026

> **Procedencia.** Este documento se redactó a partir del plan operativo del repositorio (`README.md`, v1.0 del 1 de octubre de 2026). El repositorio remite a un "documento base" (`plan-proyecto-lakehouse-financiero.md`) como fuente de verdad del alcance, pero ese archivo no está en el repositorio. Antes de entregar, el equipo debe contrastar las secciones 2 a 4 con ese documento y corregir lo que difiera.

---

## 1. Contexto y problema

Tres indicadores macroeconómicos colombianos son la base de muchos análisis financieros:

| Indicador | Periodicidad | Fuente | Forma de acceso |
|---|---|---|---|
| TRM (Tasa Representativa del Mercado) | Diaria | datos.gov.co | API Socrata |
| IPC (Índice de Precios al Consumidor) | Mensual | Banco de la República | Archivo de descarga |
| Tasa de intervención | Por decisión de la Junta (vigencia) | Banco de la República | Archivo de descarga |

**Problema.** Cada indicador vive en una fuente distinta, con un mecanismo de acceso distinto y una periodicidad distinta (diaria, mensual y por vigencia). Quien quiere compararlos hoy tiene que:

1. Descargarlos y consolidarlos a mano, sin un proceso repetible.
2. Reconciliar periodicidades incompatibles (un dato por día, uno por mes y uno por periodo de vigencia) sin una regla documentada.
3. Reportar cifras sin poder demostrar de qué fuente y transformación provienen.
4. Rehacer el trabajo cada vez que se necesita actualizar los datos.

**Enunciado del problema.** ¿Cómo integrar de forma automática, reproducible y trazable la TRM, el IPC y la tasa de intervención desde enero de 2020, de modo que un analista pueda compararlos en un mismo tablero con datos de calidad verificada?

## 2. Justificación

- **Técnica.** La arquitectura en capas (bronze → silver → gold) conserva el dato crudo, separa la limpieza del modelado analítico y permite auditar cada transformación. Las pruebas automáticas de dbt detectan duplicados, nulos y datos huérfanos antes de que lleguen al tablero.
- **De negocio.** Un modelo dimensional con un mart mensual permite comparar TRM, inflación y tasa de intervención sin que cada analista tenga que reconciliar periodicidades por su cuenta. El linaje documentado permite justificar las cifras que se reportan.
- **De reproducibilidad.** Todo el entorno se levanta con Docker Compose y un único comando de pipeline, de modo que el evaluador puede ejecutar el proyecto completo en su propia máquina (decisión D-05).
- **Académica.** El proyecto recorre el ciclo de vida completo del software (planeación, requisitos, diseño, construcción, pruebas, despliegue y cierre) con una metodología ágil, trabajo en equipo con roles definidos y evidencia en cada fase.

## 3. Objetivos

### 3.1 Objetivo general

Construir un lakehouse analítico con arquitectura moderna de capas (bronze, silver y gold): bronze en archivos Parquet inmutables por lote y silver y gold modelados con dbt sobre PostgreSQL, que ingeste, limpie, modele y visualice la TRM, el IPC y la tasa de intervención desde enero de 2020, ejecutable de punta a punta con un único comando y reproducible en la máquina del evaluador.

### 3.2 Objetivos específicos

| ID | Objetivo específico | Medida de cumplimiento | Épica / HU |
|---|---|---|---|
| OE-1 | Preparar un entorno reproducible con PostgreSQL y Metabase en Docker Compose | `docker compose up -d` crea los esquemas `bronze`, `silver` y `gold` y Metabase responde | Épica 1 · HU-01, HU-02 |
| OE-2 | Ingestar las tres fuentes en bronze conservando el dato original y sus metadatos | Registros desde el 2020-01-01 con fuente, fecha-hora de carga e identificador de lote | Épica 2 · HU-03 a HU-06 |
| OE-3 | Limpiar, tipar y deduplicar los datos en silver | Una fila por fecha (TRM), por mes (IPC) y vigencias de tasa sin solapamiento | Épica 3 · HU-07, HU-08 |
| OE-4 | Modelar un esquema estrella en gold con hechos separados por periodicidad y un mart mensual | Dimensión de fecha, hecho diario, hecho mensual y mart con una fila por mes | Épica 4 · HU-09 a HU-11 |
| OE-5 | Automatizar el flujo completo | `docker compose run --rm pipeline` ejecuta ingesta y `dbt build` y termina con código 0 | Épica 5 · HU-12 |
| OE-6 | Publicar un tablero analítico | Al menos 3 visualizaciones y filtro por rango de fechas | Épica 6 · HU-13 |
| OE-7 | Documentar y verificar el proyecto | Documentación del ciclo de vida, plan de pruebas ejecutado con evidencia y trazabilidad requisito → HU → código → prueba | Épica 7 · T-01 a T-09 |
| OE-8 | Publicar una aplicación web de consulta y extracción de los datos de gold | Se pueden ver y descargar en CSV los datos de gold filtrados por rango de fechas | Épica 6 · HU-14 |

## 4. Alcance del MVP

### 4.1 Dentro del alcance

- Tres indicadores: TRM (diaria), IPC (mensual) y tasa de intervención (por vigencia).
- Histórico desde el 1 de enero de 2020 (decisión D-02).
- Tres capas en PostgreSQL: `bronze`, `silver`, `gold`.
- Periodicidad mixta resuelta con la **Opción B**: hechos separados por periodicidad, tasa de intervención modelada por vigencia (`fecha_inicio` / `fecha_fin`) y mart mensual en gold (decisión D-03).
- Transformaciones y pruebas de calidad con dbt Core.
- Orquestación con un script Python (`pipeline.py`) y verificación local (`verificar.py`).
- Tablero en Metabase con al menos 3 visualizaciones, entregado ya cargado con datos (creado por un script contra la API de Metabase).
- Aplicación web aparte para visualizar y descargar los datos ya modelados de gold (HU-14).
- Todo el entorno en Docker: el evaluador solo necesita Docker.
- Documentación: requisitos, historias de usuario, casos de uso, diagramas, plan de pruebas, trazabilidad y manuales técnico y de usuario.

### 4.2 Fuera del alcance (se registra como "trabajo futuro")

| Elemento excluido | Origen |
|---|---|
| Integración continua (CI): las pruebas se ejecutan localmente antes de cada PR | Decisión D-07 |
| Indicadores o fuentes adicionales a los tres definidos | Riesgo "las 5 h/semana no alcanzan": alcance congelado |
| Datos anteriores a enero de 2020 (salvo el IPC desde enero de 2019, solo para calcular la inflación anual) | Decisión D-02 |
| URL directa o cambio de fuente para el IPC y la tasa de intervención (hoy se descargan a mano en CSV) | Mejora futura (decisión del PO) |
| Actualización en tiempo real o por streaming | Supuesto: la ingesta es por lotes bajo demanda |
| Modelos predictivos o de pronóstico | Supuesto: el MVP es descriptivo |
| Despliegue en la nube y gestión de usuarios o permisos | Supuesto: el sistema corre en la máquina del evaluador |

Los elementos marcados como "Supuesto" no aparecen explícitos en el repositorio. El equipo debe confirmarlos o corregirlos.

### 4.3 Criterios de éxito del MVP

El MVP se considera logrado cuando se cumplen **todos** estos criterios:

1. Las tres tablas bronze contienen datos desde el 2020-01-01 con metadatos de carga.
2. `dbt build` termina sin errores y todos los tests (`unique`, `not_null`, `relationships`) pasan.
3. `docker compose run --rm pipeline` ejecuta ingesta y `dbt build` en orden y termina con código 0.
4. Metabase muestra, ya cargado con datos, al menos 3 visualizaciones con filtro por rango de fechas.
5. Un integrante distinto de quien lo construyó instala el proyecto en una máquina limpia siguiendo solo el README (CP-INST-01).
6. La aplicación web permite ver y descargar en CSV los datos de gold filtrados por rango de fechas.

### 4.4 Restricciones y supuestos

| Tipo | Descripción |
|---|---|
| Restricción | Plan original: ~5 horas por semana por integrante. Para el calendario reajustado se estima necesario **~10 horas por semana por integrante** (~30 h/semana, ~110 h entre el 26 de octubre y el 20 de noviembre). El equipo debe confirmarlo. |
| Restricción | Una revisión intermedia (fecha por confirmar con el profesor; confirmada para el 30 de octubre de 2026, evalúa el Entregable 2) y la entrega final (20 de noviembre de 2026). |
| Restricción | Sin integración continua (D-07). |
| Restricción | El evaluador debe poder ejecutar todo en su propia máquina (D-05), con solo Docker instalado (D-09). |
| Supuesto | Las fuentes públicas (datos.gov.co y Banco de la República) permanecen disponibles y sin costo durante el proyecto. |
| Supuesto | El formato de descarga del Banco de la República es automatizable (aún por confirmar según el plan de recuperación). |

### 4.5 Partes interesadas

| Parte interesada | Rol | Interés principal |
|---|---|---|
| David Restrepo | Product Owner + desarrollador de ingesta | Priorizar el backlog y entregar bronze |
| Juan Esteban | Desarrollador (dbt) | Calidad y modelado de datos |
| Andrey Machado | Scrum Master + desarrollador (infra) | Entorno reproducible y tablero |
| Profesor | Evaluador (stakeholder externo) | Recibir las entregas y ejecutar el proyecto en su máquina |
| Analista financiero | Usuario final del tablero (rol representado) | Comparar indicadores con datos confiables |

## 5. Viabilidad del alcance

| Criterio | Evidencia | Valoración |
|---|---|---|
| Datos disponibles | Fuentes públicas y gratuitas. TRM por API y IPC y tasa por descarga | Viable. Falta confirmar el formato del Banco de la República |
| Tecnología | Herramientas abiertas y conocidas (PostgreSQL, dbt Core, Python, Docker, Metabase) | Viable. Curva de aprendizaje de dbt en Juan |
| Esfuerzo | 14 historias de usuario, 55 puntos de historia (ver `06-product-backlog.md`), en 3 sprints de construcción | Ajustado. Con ~10 h por persona alcanzan unas 110 h para 55 puntos (~1,5 h por punto) más ~30 h de documentación. El sprint 3 concentra 23 puntos |
| Tiempo | 3 sprints de una semana (26 oct – 15 nov) y una semana de cierre (16 – 20 nov) | Riesgoso. El sprint 1 cerró sin entregables técnicos y hoy (25 oct) no hay código |
| Mitigación | Alcance congelado, regla de aprobación (PO ≠ aprobador de su propio trabajo), contingencia para la fuente del Banco de la República | Definida en el plan |

**Conclusión.** El MVP es viable si el alcance se mantiene congelado y se confirma pronto el formato de descarga del Banco de la República. La contingencia, si el CSV del Banco da problemas, es entregar la TRM completa en bronze y documentar el IPC y la tasa como trabajo futuro. Orden de recorte propuesto si el tiempo no alcanza (lo decide el PO): HU-14, HU-11, HU-06.

## 6. Decisiones vigentes que condicionan el alcance

| # | Decisión | Estado |
|---|---|---|
| D-01 | Indicadores: TRM (diaria), IPC (mensual) y tasa de intervención (por decisión de la Junta) | Confirmada |
| D-02 | Histórico desde enero de 2020 | Confirmada |
| D-03 | Periodicidad mixta con la Opción B | Confirmada (falta el ADR) |
| D-04 | PostgreSQL con esquemas `bronze`, `silver`, `gold`; dbt Core; script Python; Metabase | Confirmada |
| D-05 | El evaluador ejecuta todo en su máquina | Confirmada |
| D-06 | Cada integrante sustenta su propia parte | Confirmada |
| D-07 | Sin integración continua | Confirmada |
| D-08 | GitHub Flow simplificado | Recomendada |
| D-09 | Todo el entorno y el pipeline corren en Docker; el evaluador solo necesita Docker | Confirmada (respuesta del profesor) |
| D-10 | IPC y tasa de intervención se cargan desde CSV descargados a mano y versionados en el repositorio | Confirmada (aceptada por el profesor) |
| D-11 | Aplicación web aparte para visualizar y descargar los datos de gold (HU-14) | Confirmada por el PO |
| D-12 | Arquitectura lakehouse híbrida: bronze en Parquet (fuente de verdad inmutable) replicado en PostgreSQL; silver y gold en PostgreSQL con dbt. Reemplaza a la decisión previa de llamarlo 'data warehouse' | Confirmada por el PO el 27 oct. El profesor aceptó 'el nombre más adecuado' |
