from metabase import tablero


def test_hay_al_menos_3_visualizaciones_con_el_mart_mensual():  # HU-13 escenario 1
    tarjetas = tablero.definir_tarjetas(campo_fecha=7)
    assert len(tarjetas) >= 3
    nombres = " ".join(t["name"] for t in tarjetas).lower()
    for esperado in ("trm", "inflación", "tasa"):
        assert esperado in nombres
    for t in tarjetas:
        assert "gold.mart_mensual" in t["dataset_query"]["native"]["query"]


def test_cada_tarjeta_se_filtra_por_rango_de_fechas():  # HU-13 propuesto
    for t in tablero.definir_tarjetas(campo_fecha=7):
        nativa = t["dataset_query"]["native"]
        assert "{{fechas}}" in nativa["query"]
        etiqueta = nativa["template-tags"]["fechas"]
        assert etiqueta["type"] == "dimension"
        assert etiqueta["dimension"] == ["field", 7, None]


def test_el_tablero_enlaza_el_filtro_de_fechas_a_cada_tarjeta():
    paneles = tablero.definir_paneles([11, 12, 13])
    assert [p["card_id"] for p in paneles] == [11, 12, 13]
    for p in paneles:
        (mapa,) = p["parameter_mappings"]
        assert mapa["parameter_id"] == "fechas"
        assert mapa["target"] == ["dimension", ["template-tag", "fechas"]]
