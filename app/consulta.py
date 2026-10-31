"""Consulta y extracción de datos de gold para la app web (HU-14).

Lógica sin Streamlit: filtra un conjunto de gold por rango de fechas y lo convierte a CSV.
"""

import csv
import io

from psycopg import sql

# conjunto -> (esquema, tabla, columna de fecha). El mart mensual filtra por `anio_mes` (primer día del mes).
CONJUNTOS = {
    "trm_diaria": ("gold", "fact_trm_diaria", "fecha"),
    "mart_mensual": ("gold", "mart_mensual", "anio_mes"),
}


def consultar(conexion, conjunto, desde, hasta):
    """Devuelve (columnas, filas) del conjunto con la fecha entre `desde` y `hasta`, inclusive."""
    if conjunto not in CONJUNTOS:
        raise ValueError(f"conjunto desconocido: {conjunto}")
    if desde > hasta:
        raise ValueError("rango inválido: la fecha inicial es posterior a la final")
    esquema, tabla, col_fecha = CONJUNTOS[conjunto]
    consulta = sql.SQL("select * from {}.{} where {} between %s and %s order by {}").format(
        sql.Identifier(esquema), sql.Identifier(tabla), sql.Identifier(col_fecha), sql.Identifier(col_fecha)
    )
    cursor = conexion.execute(consulta, (desde, hasta))
    return [c[0] for c in cursor.description], cursor.fetchall()


def a_csv(columnas, filas):
    """CSV con encabezado y exactamente las filas dadas; None si no hay filas (no se genera archivo)."""
    if not filas:
        return None
    salida = io.StringIO()
    escritor = csv.writer(salida, lineterminator="\n")
    escritor.writerow(columnas)
    escritor.writerows(filas)
    return salida.getvalue()
