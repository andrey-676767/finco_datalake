# Fuentes descargadas a mano (decisión D-10)

El Banco de la República no ofrece URL directa para el IPC ni para la tasa de
intervención, así que sus CSV se descargan a mano y se versionan aquí.

| Archivo | Contenido | Desde |
|---|---|---|
| `ipc.csv` | IPC mensual (índice) | enero de 2019 (para calcular la inflación anual de 2020) |
| `tasa_intervencion.csv` | Tasa de intervención por fecha de decisión o vigencia | enero de 2020 |

El archivo se versiona tal como lo entrega el Banco: no se editan columnas ni valores.
El lector acepta separador `,`, `;` o tabulador, y codificación UTF-8 o Latin-1.

## Cargar a bronze

```sh
python -m ingesta.carga_bronze ipc     # usa data/fuentes/ipc.csv
python -m ingesta.carga_bronze tasa    # usa data/fuentes/tasa_intervencion.csv
python -m ingesta.carga_bronze ipc otra/ruta.csv
```

Cada ejecución crea un lote nuevo:

- un Parquet inmutable en `data/bronze/<conjunto>/lote_id=<lote>/datos.parquet`;
- sus filas replicadas en `bronze.ipc_raw` o `bronze.tasa_intervencion_raw`.

Cada fila guarda la fuente, la fecha y hora de carga, el lote, el nombre del archivo
y su hash SHA-256. En PostgreSQL, la fila original del CSV queda completa en la
columna `fila` (`jsonb`, valores como texto).

Si el archivo no existe o no tiene filas, el comando termina con código 1 y no crea
ningún lote.
