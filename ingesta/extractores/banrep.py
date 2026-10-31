"""Lector de los CSV del Banco de la República (IPC y tasa de intervención).

El Banco no ofrece URL directa: los CSV se descargan a mano y se versionan en el
repositorio (decisión D-10). El lector no transforma nada: cada celda queda como texto
tal como viene en el archivo (por ejemplo "100,60" con coma decimal). Tipar y limpiar
es trabajo de silver.
"""

import csv
import hashlib
import io
from pathlib import Path

SEPARADORES = ",;\t"


def _decodificar(contenido):
    # Las exportaciones del Banco suelen venir en Latin-1; si el archivo es UTF-8 se respeta.
    try:
        return contenido.decode("utf-8-sig")
    except UnicodeDecodeError:
        return contenido.decode("cp1252")


def leer_csv(ruta):
    """Devuelve (filas, metadatos): filas como dicts de texto y el nombre y SHA-256 del archivo."""
    ruta = Path(ruta)
    contenido = ruta.read_bytes()
    texto = _decodificar(contenido)
    try:
        dialecto = csv.Sniffer().sniff(texto.splitlines()[0] if texto else "", delimiters=SEPARADORES)
    except csv.Error:
        dialecto = csv.excel
    filas = [dict(f) for f in csv.DictReader(io.StringIO(texto), dialect=dialecto) if any(f.values())]
    if not filas:
        raise ValueError(f"{ruta.name} no tiene filas de datos")
    return filas, {"archivo": ruta.name, "hash_archivo": hashlib.sha256(contenido).hexdigest()}
