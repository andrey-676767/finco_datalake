# App de consulta (HU-14)

`python -m streamlit run app/ui.py` (o `docker compose --profile app up app`).

El `python -m` es necesario: Streamlit agrega la carpeta del script al frente de `sys.path`, y sin la
raíz del proyecto en el path el paquete `app` no se resuelve.

Conjuntos disponibles:

- **TRM diaria** (`gold.fact_trm_diaria`), filtrada por `fecha`.
- **Mart mensual** (`gold.mart_mensual`: `anio_mes`, `trm_promedio`, `ipc`, `inflacion_anual`, `tasa_vigente`),
  filtrado por `anio_mes` (primer día de cada mes; un mes entra si su fecha está dentro de Desde–Hasta).

Elige el conjunto y el rango de fechas, revisa la vista previa y descarga el CSV con exactamente esas filas.
Si el rango no tiene datos se muestra un mensaje y no se genera archivo.
