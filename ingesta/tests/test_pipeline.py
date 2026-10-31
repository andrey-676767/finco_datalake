import pipeline


class Corredor:
    """Reemplaza subprocess.run: registra los comandos y falla en el que se le indique."""

    def __init__(self, falla_en=None, codigo=1):
        self.comandos = []
        self.falla_en = falla_en
        self.codigo = codigo

    def __call__(self, comando, **kwargs):
        self.comandos.append(comando)
        devuelve = self.codigo if self.falla_en and self.falla_en in comando else 0
        return type("R", (), {"returncode": devuelve})()


def _nombres(corredor):
    return [c[-1] if c[0] != "dbt" else "dbt" for c in corredor.comandos]


def test_ejecuta_en_orden_ingesta_de_las_fuentes_y_dbt_build(capsys):  # HU-12 escenario 1
    corredor = Corredor()
    assert pipeline.main([], correr=corredor, reloj=iter([0.0, 12.5]).__next__) == 0
    assert _nombres(corredor) == ["trm", "ipc", "tasa", "dbt", "metabase.tablero"]
    assert corredor.comandos[-2][:2] == ["dbt", "build"]


def test_informa_la_duracion_total(capsys):  # HU-12 escenario 1
    pipeline.main([], correr=Corredor(), reloj=iter([0.0, 12.5]).__next__)
    assert "Pipeline completo en 12.5 s" in capsys.readouterr().out


def test_si_la_ingesta_falla_no_ejecuta_dbt_y_dice_que_etapa_fallo(capsys):  # HU-12 propuesto
    corredor = Corredor(falla_en="ipc", codigo=3)
    assert pipeline.main([], correr=corredor, reloj=iter([0.0, 1.0]).__next__) == 3
    assert _nombres(corredor) == ["trm", "ipc"]  # no sigue con tasa ni dbt
    salida = capsys.readouterr()
    assert "error: falló la etapa «ingesta IPC»" in salida.err
    assert "Pipeline completo" not in salida.out


def test_si_dbt_falla_termina_con_su_codigo_e_indica_la_etapa(capsys):
    corredor = Corredor(falla_en="build", codigo=2)
    assert pipeline.main([], correr=corredor, reloj=iter([0.0, 1.0]).__next__) == 2
    assert "falló la etapa «dbt build»" in capsys.readouterr().err


def test_argumentos_no_esperados_muestran_el_uso(capsys):
    assert pipeline.main(["x"], correr=Corredor()) == 2
    assert capsys.readouterr().err == "uso: python pipeline.py\n"


def test_si_el_tablero_falla_indica_la_etapa(capsys):  # HU-13: tablero creado por script
    corredor = Corredor(falla_en="metabase.tablero", codigo=1)
    assert pipeline.main([], correr=corredor, reloj=iter([0.0, 1.0]).__next__) == 1
    assert "falló la etapa «tablero Metabase»" in capsys.readouterr().err
