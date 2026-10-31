# MVP data warehouse finco (HU-01, 03, 04, 05)
Orden fijado por el PO: Docker, luego ingesta. Fuente: `entregables/entregable-1/06-product-backlog.md`.

## Specs
- S1: HU-01 "Cuando ejecuto `docker compose up -d` Entonces PostgreSQL acepta conexiones con los esquemas bronze, silver y gold creados Y Metabase responde en el puerto configurado".
- S2: Se copia `.env.example` a `.env`; sin secretos reales en el repositorio.
- S3: HU-03 TRM desde 2020-01-01 en bronze, con fuente, fecha-hora de carga e identificador de lote (API ceyp-9c7c).
- S5: Arquitectura lakehouse híbrida: bronze se escribe como archivos Parquet inmutables por lote (el lake, fuente de verdad) y se replica en PostgreSQL `bronze` para que dbt construya silver y gold ahí (el house).
- S4: HU-04/05 IPC (desde 2019-01) y tasa de intervención desde CSV versionado en el repositorio, con metadatos de lote (nombre de archivo y hash).

## Tasks
- T1 (S1, S2) Docker Compose: PostgreSQL con esquemas + Metabase. [x]
- T2 (S3) Extractor TRM y carga a bronze. [x]
- T3 (S4) Cargador CSV de IPC y tasa. [x] Pendiente: versionar los CSV reales en `data/fuentes/` (descarga manual del PO).

- T4 (S5) Escribir bronze como Parquet por lote (TRM, luego IPC y tasa). [x]
- T5 (S5) Actualizar documentos y glosario: lakehouse híbrido reemplaza a D-12. [x]

## Log
- L1: "no, quiero que lo hagamos en orden" -> orden del plan de sprints, MVP primero.
- L2: "quiero que se trate como un lakehouse haciendo referencia a una arquitectura moderna" -> elegido híbrido: bronze en Parquet, silver/gold en PostgreSQL.
- L3: "si continua con t3" -> cargador genérico: la fila del CSV va completa como jsonb (texto) en PostgreSQL y como columnas de texto en Parquet. Lote con archivo y SHA-256. Los CSV reales aún no están en el repositorio.
