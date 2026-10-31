import datetime as dt

import pytest

from app import consulta


class ConexionFalsa:
    """Imita la parte de psycopg que usa consulta: execute(sql, params) -> cursor."""

    def __init__(self, columnas, filas):
        self.columnas, self.filas, self.llamadas = columnas, filas, []

    def execute(self, sentencia, params):
        self.llamadas.append((sentencia.as_string(), params))
        outer = self

        class Cursor:
            def __init__(self):
                self.description = [(c,) for c in outer.columnas]

            def fetchall(self):
                return outer.filas

        return Cursor()


def test_conjuntos_ofrece_la_trm_diaria():
    assert "trm_diaria" in consulta.CONJUNTOS


def test_consultar_filtra_por_rango_inclusivo_y_devuelve_columnas_y_filas():
    filas = [(dt.date(2023, 1, 2), 4600.5)]
    con = ConexionFalsa(["fecha", "valor"], filas)
    columnas, resultado = consulta.consultar(con, "trm_diaria", dt.date(2023, 1, 1), dt.date(2023, 12, 31))
    assert columnas == ["fecha", "valor"]
    assert resultado == filas
    sentencia, params = con.llamadas[0]
    assert "gold" in sentencia and "fact_trm_diaria" in sentencia
    assert params == (dt.date(2023, 1, 1), dt.date(2023, 12, 31))


def test_consultar_rechaza_un_conjunto_desconocido():
    with pytest.raises(ValueError, match="conjunto"):
        consulta.consultar(ConexionFalsa([], []), "otro", dt.date(2023, 1, 1), dt.date(2023, 1, 2))


def test_consultar_rechaza_rango_invertido():
    with pytest.raises(ValueError, match="rango"):
        consulta.consultar(ConexionFalsa([], []), "trm_diaria", dt.date(2023, 2, 1), dt.date(2023, 1, 1))


def test_a_csv_tiene_encabezado_y_exactamente_las_filas():
    texto = consulta.a_csv(["fecha", "valor"], [(dt.date(2023, 1, 2), 4600.5), (dt.date(2023, 1, 3), 4590)])
    assert texto.splitlines() == ["fecha,valor", "2023-01-02,4600.5", "2023-01-03,4590"]


def test_a_csv_sin_filas_no_genera_archivo():
    assert consulta.a_csv(["fecha", "valor"], []) is None


def test_conjuntos_ofrece_el_mart_mensual():
    assert "mart_mensual" in consulta.CONJUNTOS


def test_consultar_mart_mensual_filtra_por_anio_mes_y_ordena():
    filas = [(dt.date(2023, 1, 1), 4600.5, 120.1, 12.5, 11.0)]
    columnas_mart = ["anio_mes", "trm_promedio", "ipc", "inflacion_anual", "tasa_vigente"]
    con = ConexionFalsa(columnas_mart, filas)
    columnas, resultado = consulta.consultar(con, "mart_mensual", dt.date(2023, 1, 1), dt.date(2023, 6, 30))
    assert columnas == columnas_mart
    assert resultado == filas
    sentencia, params = con.llamadas[0]
    assert '"gold"."mart_mensual"' in sentencia
    assert '"anio_mes" between' in sentencia and 'order by "anio_mes"' in sentencia
    assert params == (dt.date(2023, 1, 1), dt.date(2023, 6, 30))


def test_mart_mensual_csv_tiene_exactamente_las_filas_y_vacio_no_genera_archivo():
    cols = ["anio_mes", "trm_promedio", "ipc", "inflacion_anual", "tasa_vigente"]
    texto = consulta.a_csv(cols, [(dt.date(2023, 1, 1), 4600.5, 120.1, 12.5, 11.0)])
    assert texto.splitlines() == ["anio_mes,trm_promedio,ipc,inflacion_anual,tasa_vigente", "2023-01-01,4600.5,120.1,12.5,11.0"]
    assert consulta.a_csv(cols, []) is None
