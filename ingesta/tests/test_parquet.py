import uuid
from datetime import UTC, datetime

import pyarrow.parquet as pq

from ingesta.carga_bronze import escribir_parquet

FILAS = [
    {"valor": "3158.43", "vigenciadesde": "2026-10-24T00:00:00.000", "vigenciahasta": "2026-10-26T00:00:00.000"},
    {"valor": "3185.01", "vigenciadesde": "2026-10-23T00:00:00.000", "vigenciahasta": "2026-10-23T00:00:00.000"},
]


def test_escribe_un_parquet_por_lote_con_metadatos(tmp_path):
    lote = uuid.uuid4()
    ahora = datetime(2026, 10, 27, tzinfo=UTC)
    ruta = escribir_parquet("trm", FILAS, lote, "datos.gov.co/ceyp-9c7c", ahora, tmp_path)
    assert ruta == tmp_path / "trm" / f"lote_id={lote}" / "datos.parquet"
    tabla = pq.read_table(ruta).to_pylist()
    assert len(tabla) == 2
    assert tabla[0]["valor"] == "3158.43"  # original, como texto
    assert {t["lote_id"] for t in tabla} == {str(lote)}
    assert {t["fuente"] for t in tabla} == {"datos.gov.co/ceyp-9c7c"}
    assert tabla[0]["cargado_en"] == ahora


def test_un_lote_nuevo_no_modifica_el_anterior(tmp_path):
    ahora = datetime(2026, 10, 27, tzinfo=UTC)
    l1, l2 = uuid.uuid4(), uuid.uuid4()
    r1 = escribir_parquet("trm", FILAS, l1, "f", ahora, tmp_path)
    antes = r1.read_bytes()
    escribir_parquet("trm", FILAS, l2, "f", ahora, tmp_path)
    assert r1.read_bytes() == antes


def test_el_lote_de_un_csv_guarda_archivo_y_hash(tmp_path):
    lote = uuid.uuid4()
    ahora = datetime(2026, 10, 28, tzinfo=UTC)
    meta = {"archivo": "ipc.csv", "hash_archivo": "abc123"}
    ruta = escribir_parquet("ipc", [{"Índice": "100,60"}], lote, "f", ahora, tmp_path, meta)
    tabla = pq.read_table(ruta).to_pylist()
    assert tabla == [
        {"Índice": "100,60", "lote_id": str(lote), "fuente": "f", "cargado_en": ahora,
         "archivo": "ipc.csv", "hash_archivo": "abc123"}
    ]
