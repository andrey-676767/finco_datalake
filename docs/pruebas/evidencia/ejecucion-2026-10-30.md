# Evidencia de ejecución de pruebas (T-07), 30 oct 2026

Ejecutado sobre `main` (commit `3b31b45`) en local, con Docker 29.7.2 y el entorno de
`docker-compose.yml` (PostgreSQL 16 y Metabase v0.50.36 arriba).

## Pipeline completo en Docker (CP-E2E-01)

```
$ docker compose run --rm pipeline
==> ingesta TRM
==> ingesta IPC
==> ingesta tasa de intervención
==> dbt build
Done. PASS=42 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=42
==> tablero Metabase
El tablero «Tablero macroeconómico» ya existe; no se crea otro.
Pipeline completo en 12.0 s
```

Código de salida 0. Las cinco etapas corrieron en orden, incluido el tablero.

## Datos cargados

| Tabla | Filas |
|---|---|
| `bronze.trm_raw` | 8084 |
| `bronze.ipc_raw` | 2601 |
| `bronze.tasa_intervencion_raw` | 31455 |
| `silver.trm` | 2493 |
| `silver.ipc` | 93 |
| `silver.tasa_intervencion` | 36 |
| `gold.dim_fecha` | 2860 |
| `gold.fact_trm_diaria` | 2493 |
| `gold.fact_indicadores_mensual` | 81 |
| `gold.mart_mensual` | 81 |

Las tablas bronze acumulan lotes de cargas anteriores; silver y gold quedan deduplicadas.

## Tablero de Metabase (CP-DASH-01)

Consultado por la API de Metabase con el usuario administrador de `.env`:

- Tablero «Tablero macroeconómico» (id 2), parámetro `Fechas`.
- Tres visualizaciones de línea, todas con datos (81 filas cada una, desde `2020-01-01`):
  - «Inflación anual (%)» — `inflacion_anual`
  - «Evolución de la TRM (promedio mensual)» — `trm_promedio`
  - «Tasa de intervención frente a inflación (%)» — `tasa_vigente`, `inflacion_anual`

## Aplicación web (CP-APP-01)

```
$ docker compose --profile app up -d app
$ curl -o /dev/null -w '%{http_code}' http://127.0.0.1:8501/
200
```

La interfaz responde; la descarga del CSV filtrado y el aviso sin datos están cubiertos por
`app/tests/test_consulta.py`.

## Verificación local

```
$ python -m pytest -q
39 passed, 4 skipped in 0.56s
```

Los 4 omitidos son los casos de integración de `ingesta/tests/test_carga_bronze.py`, que
requieren PostgreSQL en el puerto del `.env`; con el entorno arriba corren dentro del
pipeline.

## Sin ejecutar

- CP-INST-01 (HU-02): instalación en una máquina limpia, sin datos ni contenedores previos.
  Esta corrida reutilizó el entorno ya levantado, así que no sustituye esa prueba.
