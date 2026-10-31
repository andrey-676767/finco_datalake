import hashlib

import pytest

from ingesta.extractores.banrep import leer_csv

# Exportación típica del Banco de la República: separador ";", coma decimal y Latin-1.
IPC_BANREP = "Año(aaaa)-Mes(mm);Índice\n2019-01;100,60\n2019-02;101,18\n".encode("latin-1")


def test_lee_el_csv_sin_transformar_y_calcula_el_hash(tmp_path):
    ruta = tmp_path / "ipc.csv"
    ruta.write_bytes(IPC_BANREP)
    filas, meta = leer_csv(ruta)
    assert filas == [
        {"Año(aaaa)-Mes(mm)": "2019-01", "Índice": "100,60"},  # valor original, como texto
        {"Año(aaaa)-Mes(mm)": "2019-02", "Índice": "101,18"},
    ]
    assert meta == {"archivo": "ipc.csv", "hash_archivo": hashlib.sha256(IPC_BANREP).hexdigest()}


def test_acepta_csv_utf8_separado_por_comas(tmp_path):
    ruta = tmp_path / "tasa.csv"
    ruta.write_text("Fecha,Tasa de intervención\n2020-01-01,4.25\n", encoding="utf-8-sig")
    filas, _ = leer_csv(ruta)
    assert filas == [{"Fecha": "2020-01-01", "Tasa de intervención": "4.25"}]


def test_un_csv_sin_filas_es_un_error(tmp_path):
    ruta = tmp_path / "vacio.csv"
    ruta.write_text("Fecha;Valor\n", encoding="utf-8")
    with pytest.raises(ValueError, match="vacio.csv no tiene filas de datos"):
        leer_csv(ruta)
