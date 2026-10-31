"""Prueba de humo de la app web (HU-14): el script de Streamlit se ejecuta sin excepciones.

Regresión: el entrypoint se llamaba `app/app.py`, igual que el paquete. Streamlit pone la carpeta
del script al frente de `sys.path`, así que `from app import consulta` resolvía al propio script y
la app fallaba con `partially initialized module 'app'`.
"""

import os
from pathlib import Path

import pytest

psycopg = pytest.importorskip("psycopg")
pytest.importorskip("streamlit")

from streamlit.testing.v1 import AppTest

RUTA = Path(__file__).resolve().parents[1] / "ui.py"


@pytest.fixture(autouse=True)
def requiere_postgres():
    try:
        conexion = psycopg.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            dbname=os.environ["POSTGRES_DB"],
        )
    except KeyError:
        pytest.skip("faltan las variables POSTGRES_*")
    except psycopg.OperationalError:
        pytest.skip("PostgreSQL no disponible (docker compose up -d)")
    conexion.close()


def test_el_paquete_app_apunta_al_paquete_y_no_al_script():
    import app

    assert Path(app.__file__).name == "__init__.py"


def test_el_script_se_ejecuta_sin_excepciones():
    at = AppTest.from_file(str(RUTA))
    at.run()

    assert not at.exception, [str(e.value) for e in at.exception]
    assert len(at.selectbox) == 1
