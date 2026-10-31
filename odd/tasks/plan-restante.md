# Plan restante hasta la entrega final (20 nov)
Fuentes: `entregables/entregable-1/02-planeacion-cronograma.md` (Gantt) y `entregables/entregable-1/06-product-backlog.md` (criterios). Complementa `mvp-datawarehouse.md`.
Estado al 2026-10-30: todas las HU de HU-01 y HU-03 a HU-14 están en `main` (PRs #1 a #22). Solo queda HU-02 y el cierre documental.

## Specs
- S1: HU-04/05 "el CSV de IPC exportado del Banco de la República (desde enero de 2019) está versionado en el repositorio" y "el CSV de tasa de intervención exportado del Banco de la República está versionado en el repositorio".
- S2: HU-08 "cada registro tiene fecha_inicio y fecha_fin de vigencia Y los periodos de vigencia no se solapan".
- S3: HU-09 "existe una dimensión de fecha, un hecho diario de TRM y un hecho mensual de indicadores Y el mart mensual tiene una fila por mes con TRM promedio, IPC y tasa vigente".
- S4: HU-12 "se ejecutan en orden la ingesta de las 2 fuentes y "dbt build"" (hoy solo cubre TRM).
- S5: HU-06 "reintenta al menos 3 veces con espera creciente Y si todos los intentos fallan, registra el error en el log y termina con código distinto de 0".
- S6: HU-11 "el grafo de linaje muestra el camino desde las tablas bronze hasta el mart Y cada columna del mart tiene una descripción que indica su origen".
- S7: HU-13 "al menos 3 visualizaciones: evolución de la TRM, inflación anual y tasa de intervención frente a inflación Y puedo filtrar por rango de fechas Y el tablero fue creado automáticamente por un script contra la API de Metabase, sin pasos manuales".
- S8: HU-02 "Dado una máquina con solo Docker instalado y sin datos previos del proyecto Cuando sigo los pasos del README en orden Entonces el pipeline termina sin errores Y puedo abrir el tablero con datos cargados y usar la aplicación web".
- S9: Tareas de documentación T-02 a T-09 (backlog, Épica 7).

## Tasks (ID, specs, responsable, fecha Gantt)
### Sprint 2 (hasta 1 nov)
- T1 (S1) Versionar CSV reales de IPC y tasa en `data/fuentes/` y cargarlos. David, 30 oct–1 nov. [x] `data/fuentes/ipc.csv` y `tasa_intervencion.csv` versionados (PR #10).
- T2 (S9) T-02 Casos de uso y flujos (`docs/diseno/casos-uso.md`). David, hasta 8 nov. [x] commit docs: casos de uso y flujos.
- T3 (S9) T-03 Diagrama de arquitectura. Andrey, 29 oct–1 nov. [x] `docs/diseno/arquitectura.md`.
- T4 (S9) T-04 ER de 3 capas y ADR Opción B. Juan, 26 oct–1 nov. [x] `docs/diseno/modelo-datos.md`.
### Sprint 3 (2–8 nov)
- T5 (S2) HU-08 Silver de IPC y tasa por vigencia. Juan, 3–6 nov. [x] PR #14.
- T6 (S3) HU-09 Hecho mensual y mart mensual. Juan, 4–8 nov. [x] PR #22.
- T7 (S4) HU-12 Pipeline con IPC y tasa. Andrey, 4–8 nov. [x] PR #12; verificado en Docker el 30 oct (12.0 s).
- T8 (S5) HU-06 Reintentos y log de errores en TRM. David, 2–4 nov. [x] PR #8.
- T9 (S9) T-06 Plan de pruebas y casos. Juan, 2–6 nov. [x] `docs/pruebas/plan-pruebas.md`.
- T10 (S9) T-05 Matriz de trazabilidad v1 (`docs/gestion/trazabilidad.md`). Andrey, 5–8 nov. [x] v2 al 30 oct.
### Sprint 4 (9–15 nov)
- T11 (S7) HU-13 Tablero Metabase por script. Andrey, 9–13 nov. [x] PR #16 y #18; verificado por API el 30 oct.
- T12 (S6) HU-11 Linaje con dbt docs. Juan, 9–11 nov. [x] PR #17.
- T13 (S9) T-07 Ejecución de pruebas y evidencia. Juan, 10–15 nov. [x] `docs/pruebas/evidencia/ejecucion-2026-10-29.md` y `-10-30.md`.
- T14 (S9) T-08 Manual técnico y de usuario. Andrey, 11–15 nov. [x] `docs/manuales/manual.md` (PR #21).
- T15 HU-14 Actualizar la app para leer el mart mensual. David. [x] PR #13 y #19.
### Cierre (16–20 nov)
- T16 (S8) HU-02 Instalación en máquina limpia con solo el README. Andrey, 16–18 nov. [x] corrida en clon limpio el 30 oct: pasa; evidencia en `docs/pruebas/evidencia/ejecucion-2026-10-30-instalacion-limpia.md`.
- T17 (S9) T-09 Trazabilidad final, actas, retrospectiva. Andrey/todos, 16–19 nov. [x] `docs/gestion/trazabilidad.md` y `docs/gestion/actas-retrospectiva.md`; solo falta que el equipo complete lo marcado «A confirmar».
- T18 Ensayo de demo. Todos, 18–19 nov. [ ]

## Log
- L1: "no hay un plan definido para cumplir con las histirias de usuarios y las tareas ?"
- L2: "si" (crear el documento con HU y T-xx pendientes, fecha del Gantt y criterio del backlog).
- L3 (30 oct 2026): estado sincronizado con `main`; se marcan T1–T15 y se corrigen los comentarios que decían "sin PR". Quedan T16 (HU-02), T17 (actas y retrospectiva) y T18 (ensayo de demo).
