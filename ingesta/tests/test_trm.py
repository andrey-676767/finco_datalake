
import pytest
import requests

from ingesta.extractores.trm_socrata import FECHA_INICIO, ExtraccionError, extraer_trm


class FakeResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self._data


class FakeSession:
    """Simula la API Socrata sin red: devuelve `filas` paginadas por $limit/$offset."""

    def __init__(self, filas):
        self.filas = filas
        self.llamadas = []

    def get(self, url, params=None, timeout=None):
        self.llamadas.append(params)
        offset, limit = int(params["$offset"]), int(params["$limit"])
        return FakeResponse(self.filas[offset : offset + limit])


def _filas(n):
    return [
        {"valor": str(3000 + i), "vigenciadesde": f"d{i}", "vigenciahasta": f"h{i}"}
        for i in range(n)
    ]


def test_recorre_todas_las_paginas():  # CP-ING-01
    sesion = FakeSession(_filas(25))
    resultado = extraer_trm(sesion, tam_pagina=10)
    assert resultado == _filas(25)
    assert [p["$offset"] for p in sesion.llamadas] == [0, 10, 20]


def test_filtra_desde_2020_y_ordena():
    sesion = FakeSession(_filas(3))
    extraer_trm(sesion, tam_pagina=10)
    assert FECHA_INICIO == "2020-01-01"
    assert "2020-01-01" in sesion.llamadas[0]["$where"]
    assert sesion.llamadas[0]["$order"] == "vigenciadesde"


def test_conserva_el_valor_original_sin_transformar():
    filas = [{"valor": "3158.43", "vigenciadesde": "x", "vigenciahasta": "y"}]
    assert extraer_trm(FakeSession(filas))[0]["valor"] == "3158.43"


# --- HU-06: reintentos y registro de errores ---


class SesionQueFalla(FakeSession):
    """Falla las primeras `fallos` llamadas (por red o por HTTP) y luego responde normal."""

    def __init__(self, filas, fallos, error=None):
        super().__init__(filas)
        self.fallos = fallos
        self.error = error or requests.ConnectionError("sin red")
        self.intentos = 0

    def get(self, url, params=None, timeout=None):
        self.intentos += 1
        if self.intentos <= self.fallos:
            raise self.error
        return super().get(url, params, timeout)


def test_reintenta_tras_una_falla_temporal_y_devuelve_los_datos():  # HU-06
    esperas = []
    sesion = SesionQueFalla(_filas(3), fallos=1)
    assert extraer_trm(sesion, tam_pagina=10, espera=esperas.append) == _filas(3)
    assert sesion.intentos == 2


def test_reintenta_al_menos_3_veces_con_espera_creciente():  # HU-06
    esperas = []
    sesion = SesionQueFalla(_filas(3), fallos=3)
    assert extraer_trm(sesion, tam_pagina=10, espera=esperas.append) == _filas(3)
    assert sesion.intentos == 4  # 1 intento + 3 reintentos
    assert esperas == sorted(set(esperas)) and len(esperas) == 3  # estrictamente creciente


def test_un_error_http_tambien_se_reintenta():  # HU-06
    sesion = SesionQueFalla(_filas(3), fallos=1, error=requests.HTTPError("503"))
    assert extraer_trm(sesion, tam_pagina=10, espera=lambda s: None) == _filas(3)


def test_si_todos_los_intentos_fallan_registra_el_error_y_lanza(caplog):  # HU-06
    sesion = SesionQueFalla(_filas(3), fallos=99)
    with caplog.at_level("ERROR"), pytest.raises(ExtraccionError, match="4 intentos"):
        extraer_trm(sesion, tam_pagina=10, espera=lambda s: None)
    assert sesion.intentos == 4
    assert "sin red" in caplog.text


def test_la_falla_en_una_pagina_intermedia_no_duplica_ni_pierde_filas():  # HU-06
    class FallaEnLaSegundaPagina(FakeSession):
        def __init__(self, filas):
            super().__init__(filas)
            self.fallo = False

        def get(self, url, params=None, timeout=None):
            if int(params["$offset"]) == 10 and not self.fallo:
                self.fallo = True
                raise requests.Timeout("lento")
            return super().get(url, params, timeout)

    sesion = FallaEnLaSegundaPagina(_filas(25))
    assert extraer_trm(sesion, tam_pagina=10, espera=lambda s: None) == _filas(25)
