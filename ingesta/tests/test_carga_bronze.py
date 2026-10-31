import pytest

psycopg = pytest.importorskip("psycopg")

from ingesta.carga_bronze import cargar_trm, conectar, crear_tablas

FILAS = [
    {"valor": "3158.43", "vigenciadesde": "2026-10-24T00:00:00.000", "vigenciahasta": "2026-10-26T00:00:00.000"},
    {"valor": "3185.01", "vigenciadesde": "2026-10-23T00:00:00.000", "vigenciahasta": "2026-10-23T00:00:00.000"},
]


@pytest.fixture
def conn():
    try:
        c = conectar()
    except psycopg.OperationalError:
        pytest.skip("PostgreSQL no disponible (docker compose up -d)")
    crear_tablas(c)
    yield c
    c.rollback()  # nada de la prueba queda en la base
    c.close()


def test_cada_registro_tiene_fuente_fecha_de_carga_y_lote(conn):  # CP-ING-03
    lote = cargar_trm(conn, FILAS)
    filas = conn.execute(
        "select fuente, cargado_en, lote_id, valor from bronze.trm_raw where lote_id = %s order by valor",
        (lote,),
    ).fetchall()
    assert len(filas) == 2
    for fuente, cargado_en, lote_id, _ in filas:
        assert fuente == "datos.gov.co/ceyp-9c7c"
        assert cargado_en is not None
        assert lote_id == lote
    assert [f[3] for f in filas] == ["3158.43", "3185.01"]  # valor original, como texto


def test_nueva_ejecucion_crea_lote_nuevo_sin_tocar_el_anterior(conn):
    lote1 = cargar_trm(conn, FILAS)
    antes = conn.execute("select * from bronze.trm_raw where lote_id = %s order by id", (lote1,)).fetchall()
    lote2 = cargar_trm(conn, FILAS)
    assert lote2 != lote1
    despues = conn.execute("select * from bronze.trm_raw where lote_id = %s order by id", (lote1,)).fetchall()
    assert antes == despues


def test_csv_en_bronze_con_metadatos_de_lote_archivo_y_hash(conn):  # CP-ING-03, HU-04/05
    from ingesta.carga_bronze import FUENTE_IPC, cargar_csv

    filas = [{"Año(aaaa)-Mes(mm)": "2019-01", "Índice": "100,60"}, {"Año(aaaa)-Mes(mm)": "2019-02", "Índice": "101,18"}]
    meta = {"archivo": "ipc.csv", "hash_archivo": "abc123"}
    lote = cargar_csv(conn, "ipc", filas, meta)
    guardadas = conn.execute(
        "select fuente, cargado_en, lote_id, archivo, hash_archivo, numero_fila, fila"
        " from bronze.ipc_raw where lote_id = %s order by numero_fila",
        (lote,),
    ).fetchall()
    assert [(g[0], g[2], g[3], g[4], g[5], g[6]) for g in guardadas] == [
        (FUENTE_IPC, lote, "ipc.csv", "abc123", 1, filas[0]),
        (FUENTE_IPC, lote, "ipc.csv", "abc123", 2, filas[1]),
    ]
    assert all(g[1] is not None for g in guardadas)


def test_csv_nueva_carga_crea_lote_nuevo_sin_tocar_el_anterior(conn):
    from ingesta.carga_bronze import cargar_csv

    filas = [{"Fecha": "2020-01-01", "Tasa": "4,25"}]
    meta = {"archivo": "tasa_intervencion.csv", "hash_archivo": "h"}
    lote1 = cargar_csv(conn, "tasa_intervencion", filas, meta)
    antes = conn.execute("select * from bronze.tasa_intervencion_raw where lote_id = %s", (lote1,)).fetchall()
    lote2 = cargar_csv(conn, "tasa_intervencion", filas, meta)
    assert lote2 != lote1
    assert conn.execute("select * from bronze.tasa_intervencion_raw where lote_id = %s", (lote1,)).fetchall() == antes
