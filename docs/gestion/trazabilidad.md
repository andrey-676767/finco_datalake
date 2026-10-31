# Matriz de trazabilidad v2 (T-05, T-09)

Estado al 30 oct 2026. "Hecho" significa implementado,
mergeado y verificado en `main`.
La evidencia de las corridas está en `docs/pruebas/evidencia/ejecucion-2026-10-30.md`.

| Requisito | HU | Casos de uso | Caso de prueba | Implementación | Estado |
|---|---|---|---|---|---|
| RF-01 | HU-03, 04, 05, 06 | CU-03 | CP-ING-01, 02 | `ingesta/`, `data/fuentes/` | Hecho (PR #3, #8, #10) |
| RF-01b | HU-08, 09 | CU-04 | CP-SIL-02, CP-GLD-02 | `dbt/models/silver/`, `dbt/models/gold/` | Hecho (PR #14, #22) |
| RF-02 | HU-03, 04, 05 | CU-03 | CP-ING-03 | `ingesta/carga_bronze.py`, `data/bronze/` | Hecho |
| RF-03 | HU-07, 08 | CU-04 | CP-SIL-01 | `dbt/models/silver/` | Hecho (PR #7, #14) |
| RF-04 | HU-09 | CU-04 | CP-GLD-02 | `dbt/models/gold/` | Hecho (PR #9, #22) |
| RF-05 | HU-07, 08, 10 | CU-04 | CP-SIL-01, CP-GLD-01 | tests en `*.yml` de dbt | Hecho |
| RF-06 | HU-11 | CU-07 | Aceptación de HU-11 | `dbt docs` | Hecho (PR #17) |
| RF-07 | HU-13 | CU-05 | CP-DASH-01 | Metabase | Hecho y verificado por API (PR #16, #18) |
| RF-08 | HU-12, 02 | CU-02, CU-08 | CP-E2E-01 | `pipeline.py`, `verificar.py` | Hecho y verificado (HU-12 y HU-02) |
| RF-09 | HU-14 | CU-06 | CP-APP-01 | `app/` | Hecho (PR #13, #19) |
| RNF-01 | HU-01, 02 | CU-01, CU-08 | CP-INST-01 | `docker-compose.yml`, `Dockerfile` | Hecho y verificado en clon limpio (HU-01 y HU-02) |
| RNF-02 | HU-12 | CU-02 | CP-E2E-01 | `pipeline.py` | Medido: 12.0 s (umbral < 5 min) |
| RNF-03 | Todas | — | `verificar.py` | ruff | Hecho |
| RNF-04 | Todas | — | Historial de Git | PRs enlazados a HU | Hecho |
| RNF-05 | HU-11 | CU-07 | Aceptación de HU-11 | `dbt docs` | Hecho (PR #17) |

## Cierre

- **HU-02 / CP-INST-01:** pasa en clon limpio (`docs/pruebas/evidencia/ejecucion-2026-10-30-instalacion-limpia.md`).
  La corrida encontró que el tablero fallaba por falta de healthcheck en Metabase; corregido.
- **T-09:** actas de sprint y retrospectiva en `docs/gestion/actas-retrospectiva.md`; las opiniones del equipo quedan «A confirmar».
- **CP-GLD-02:** fijado con `dbt/tests/mart_mensual_empieza_en_2020_01.sql`.

Todas las HU (HU-01 a HU-14) están en `main`.

## Diagramas del Entregable 2

El detalle de cada caso de uso con sus diagramas, HU y pruebas está en
`entregables/entregable-2/00-indice.md`. Casos de prueba agregados: CP-PIPE-01, CP-DASH-02, CP-LIN-01 y CP-CAL-01
(ver `docs/pruebas/plan-pruebas.md`).
