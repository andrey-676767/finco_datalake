# Actas de sprint y retrospectiva (T-09)

Redactadas el 30 oct 2026 solo con hechos verificables del repositorio (PR, commits, evidencia).
Lo que dependía de la reunión del equipo (asistentes, opiniones) no se inventó: está marcado
**«A confirmar»** para que el equipo lo complete en la reunión del cierre.

> **Nota de fechas.** Todos los PR de los sprints 2 a 4 se integraron entre el 27 y el 30 oct, antes
> de lo previsto en el cronograma. Cada acta agrupa el trabajo por el sprint al que pertenecía en el plan.

## Acta del sprint 1 (21 sep – 25 oct)

- **Objetivo:** planeación y requisitos en borrador (documentos 00 a 06).
- **Resultado:** documentos entregados; sin repositorio funcional, Docker ni código.
- **Impedimento:** el retraso técnico obligó a comprimir los sprints 2 a 4 a una semana cada uno
  (`entregables/entregable-1/02-planeacion-cronograma.md`). Alcance y objetivos sin cambios, salvo la HU-14 pedida por el PO el 25 oct.
- Asistentes y decisiones de la reunión: **A confirmar.**

## Acta del sprint 2 (26 oct – 1 nov): Docker y bronze

- **Entregado en `main`:** HU-01 Docker Compose (PR #1), HU-03 TRM en bronze (PR #3), bronze en Parquet
  por lote, HU-04/05 CSV de IPC y tasa (PR #10), HU-07 TRM en silver (PR #7), diseño T-02 a T-04 (PR #11).
- **Decisión:** arquitectura lakehouse híbrida (bronze en Parquet y PostgreSQL; silver y gold en PostgreSQL),
  documentada en `docs/diseno/modelo-datos.md`.
- **Corrección:** restauración de bronze Parquet/CSV (PR #6).

## Acta del sprint 3 (2 – 8 nov): silver, gold y pipeline

- **Entregado en `main`:** HU-06 reintentos (PR #8), HU-08 silver de IPC y tasa (PR #14), HU-09/10 gold y
  pruebas `relationships` (PR #9, #22), HU-12 pipeline de un comando (PR #12).
- **Verificación:** `python verificar.py` en verde; `dbt build` con PASS=42 ERROR=0.

## Acta del sprint 4 (9 – 15 nov): tablero, app y pruebas

- **Entregado en `main`:** HU-13 tablero por script (PR #16, #18), HU-11 linaje (PR #17),
  HU-14 app Streamlit (PR #13, #19), manual (PR #21), plan de pruebas y trazabilidad (PR #20).
- **Evidencia:** `docs/pruebas/evidencia/ejecucion-2026-10-29.md` y `ejecucion-2026-10-30.md`.
- **Corrección posterior:** el entrypoint `app/app.py` chocaba con el paquete `app` en Streamlit; se
  renombró a `app/ui.py` con prueba de regresión.

## Retrospectiva general

**Qué funcionó**
- Alcance cerrado por historias con Gherkin y PR pequeños enlazados a cada HU.
- `verificar.py` reemplazó la integración continua: ruff, pytest y `dbt build` antes de cada PR.
- El pipeline completo corre con un comando en Docker en 12 s (umbral: 5 min).
- El tablero se crea por script contra la API de Metabase, sin pasos manuales.

**Qué no funcionó**
- El sprint 1 cerró sin código; el calendario original dejó de ser alcanzable.
- La app tuvo un defecto de arranque que las pruebas unitarias no detectaron; solo la prueba de humo con Streamlit lo cubre.
- Los CSV de IPC y tasa se descargan a mano del Banco de la República.

**Mejoras para un próximo proyecto**
- Levantar el entorno Docker y un pipeline mínimo en el primer sprint.
- Probar el arranque de cada servicio, no solo sus funciones.

**Opiniones del equipo sobre la dinámica de trabajo:** A confirmar.

## Trabajo futuro

- Automatizar la descarga de IPC y tasa (hoy son CSV versionados).
- Integración continua que ejecute `verificar.py`.
- Programar el pipeline de forma periódica.
- Alertas de calidad de datos.
