from ingesta.carga_bronze import main

USO = "uso: python -m ingesta.carga_bronze trm | ipc [ruta.csv] | tasa [ruta.csv]\n"


def test_argumentos_invalidos_muestran_el_uso(capsys):
    assert main(["otra"]) == 2
    salida = capsys.readouterr()
    assert (salida.out, salida.err) == ("", USO)


def test_sin_argumentos_muestra_el_uso(capsys):  # comportamiento previo de trm
    assert main([]) == 2
    assert capsys.readouterr().err == USO


def test_csv_inexistente_termina_con_error_sin_crear_lote(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr("ingesta.carga_bronze.RAIZ_LAKE", tmp_path)
    ruta = tmp_path / "no-existe.csv"
    assert main(["ipc", str(ruta)]) == 1
    salida = capsys.readouterr()
    assert (salida.out, salida.err) == ("", f"error: no existe el archivo {ruta}\n")
    assert list(tmp_path.iterdir()) == []  # no se escribió ningún lote


def test_trm_que_no_se_puede_extraer_termina_con_error_sin_crear_lote(tmp_path, capsys, monkeypatch):  # HU-06
    from ingesta.extractores.trm_socrata import ExtraccionError

    def falla():
        raise ExtraccionError("no se pudo extraer la TRM tras 4 intentos: sin red")

    monkeypatch.setattr("ingesta.carga_bronze.RAIZ_LAKE", tmp_path)
    monkeypatch.setattr("ingesta.extractores.trm_socrata.extraer_trm", falla)
    assert main(["trm"]) == 1
    salida = capsys.readouterr()
    assert (salida.out, salida.err) == ("", "error: no se pudo extraer la TRM tras 4 intentos: sin red\n")
    assert list(tmp_path.iterdir()) == []
