# Evidencia de ejecución de pruebas (T-07), 29 oct 2026

Ejecutado en local contra PostgreSQL de Docker con los datos reales cargados.

| Rama | ruff | pytest | dbt build |
|---|---|---|---|
| `feature/HU-13-tablero` (silver, gold, mart, tablero) | OK | 19 passed | PASS=42, ERROR=0 |
| `feature/HU-14b-app-mart` (app, pipeline, `verificar.py`) | OK | 33 passed | PASS=17, ERROR=0 |

`python verificar.py` terminó con "Todo en orden" en `feature/HU-14b-app-mart`.
`feature/HU-13-tablero` no tiene `verificar.py` (se ramificó antes de HU-12); se corrieron sus tres comandos a mano.

## Sin ejecutar
- Ninguna rama integrada: las ramas aún no están mergeadas, así que no hay una corrida única de todo el proyecto.
- CP-E2E-01 (`docker compose run --rm pipeline`), CP-DASH-01 en navegador, CP-INST-01 y la UI de Streamlit.
