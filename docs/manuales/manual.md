# Manual técnico y de usuario (T-08)

## Manual de usuario

### Requisitos
Solo Docker con Compose.

### Instalación y ejecución
```sh
cp .env.example .env
docker compose up -d                      # PostgreSQL (esquemas bronze, silver, gold) y Metabase
docker compose run --rm pipeline          # ingesta de TRM, IPC y tasa + dbt build + tablero
docker compose --profile app up app       # app web: http://localhost:8501
```

### Qué se obtiene
- **Tablero (Metabase):** http://localhost:3000, tablero «Tablero macroeconómico» con filtro de fechas.
  Se crea automáticamente al final del pipeline (`metabase/tablero.py`, con `METABASE_ADMIN_EMAIL` y
  `METABASE_ADMIN_PASSWORD` de `.env`); si ya existe, no lo duplica.
- **App web (Streamlit):** elegir conjunto (TRM diaria o mart mensual), rango de fechas, ver la vista previa y descargar el CSV.
  Si el rango no tiene datos, muestra un mensaje y no genera archivo.
- **Linaje:** `cd dbt && dbt docs generate --profiles-dir . && dbt docs serve --profiles-dir .`

## Manual técnico

### Arquitectura
Ver `docs/diseno/arquitectura.md` (lakehouse híbrido: bronze en Parquet y PostgreSQL; silver y gold con dbt) y `docs/diseno/modelo-datos.md`.

### Estructura
| Ruta | Contenido |
|---|---|
| `ingesta/` | Extractor TRM y cargador de CSV a bronze |
| `data/fuentes/` | CSV de IPC y tasa del Banco de la República |
| `dbt/` | Modelos silver y gold, pruebas y linaje |
| `metabase/` | Script que crea el tablero por la API |
| `app/` | Aplicación Streamlit |
| `pipeline.py`, `verificar.py` | Pipeline de un comando y verificación local |

### Verificación local
`python verificar.py` corre ruff, pytest y `dbt build` (requiere `.env` exportado y PostgreSQL arriba).

### Limitaciones conocidas
- El tablero no tiene respaldo fuera de la base interna de Metabase: si se borra el volumen `pgdata`, hay que volver a correr el pipeline para recrearlo.
- Las instrucciones no se han probado en una máquina limpia (HU-02).
