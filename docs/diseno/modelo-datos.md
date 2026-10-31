# Modelo de datos y ADR-01 (T-04)

## 1. Capas

```mermaid
erDiagram
    BRONZE_TRM_RAW { text id text valor text vigenciadesde text vigenciahasta uuid lote_id timestamptz cargado_en }
    BRONZE_IPC_RAW { jsonb fila uuid lote_id timestamptz cargado_en text archivo text hash }
    BRONZE_TASA_RAW { jsonb fila uuid lote_id timestamptz cargado_en text archivo text hash }
    SILVER_TRM { date fecha numeric valor date vigencia_desde date vigencia_hasta uuid lote_id }
    SILVER_IPC { date mes numeric indice }
    SILVER_TASA { date fecha_inicio date fecha_fin numeric tasa }
    DIM_FECHA { date fecha int anio int mes date anio_mes }
    FACT_TRM_DIARIA { date fecha numeric valor }
    FACT_INDICADORES_MENSUAL { date anio_mes numeric ipc numeric inflacion_anual numeric tasa_vigente }
    MART_MENSUAL { date anio_mes numeric trm_promedio numeric ipc numeric tasa_vigente }
    BRONZE_TRM_RAW ||--o{ SILVER_TRM : dbt
    BRONZE_IPC_RAW ||--o{ SILVER_IPC : dbt
    BRONZE_TASA_RAW ||--o{ SILVER_TASA : dbt
    DIM_FECHA ||--o{ FACT_TRM_DIARIA : fecha
    DIM_FECHA ||--o{ FACT_INDICADORES_MENSUAL : anio_mes
    FACT_TRM_DIARIA ||--o{ MART_MENSUAL : promedio
    FACT_INDICADORES_MENSUAL ||--|| MART_MENSUAL : anio_mes
```

Todas las tablas del diagrama están implementadas (`bronze`, `silver` y `gold`, ver `dbt/models/`). Las columnas del diagrama son ilustrativas; las definitivas están en los `.yml` de dbt.

## 2. ADR-01 Periodicidad mixta: Opción B (D-03)

- **Contexto:** la TRM es diaria, el IPC mensual y la tasa de intervención cambia por decisión (vigencia).
- **Decisión:** hechos separados por periodicidad; la tasa se modela con `fecha_inicio` y `fecha_fin` sin solapes; un mart mensual en gold une TRM promedio, IPC y tasa vigente.
- **Alternativas descartadas:** (A) un único hecho diario repitiendo IPC y tasa: duplica valores y confunde la granularidad; no se detalló otra en los documentos del repositorio.
- **Consecuencias:** más tablas, pero cada hecho conserva su granularidad real; la tasa vigente de un mes se resuelve por intersección de vigencia.
- **Estado:** confirmada por el equipo.
