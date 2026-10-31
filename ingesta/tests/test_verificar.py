import verificar
from ingesta.tests.test_pipeline import Corredor


def test_corre_todas_las_verificaciones_y_termina_con_0_si_pasan(capsys):
    corredor = Corredor()
    assert verificar.main([], correr=corredor) == 0
    nombres = ["pytest" if c[1:3] == ["-m", "pytest"] else c[0] for c in corredor.comandos]
    assert nombres == ["ruff", "pytest", "dbt"]
    assert "Todo en orden" in capsys.readouterr().out


def test_si_una_falla_sigue_con_las_demas_y_termina_distinto_de_0(capsys):
    corredor = Corredor(falla_en="check")  # ruff check
    assert verificar.main([], correr=corredor) == 1
    assert len(corredor.comandos) == 3  # no se detiene en la primera
    assert "Fallaron: ruff" in capsys.readouterr().err


def test_pytest_se_invoca_como_modulo_para_ver_la_raiz_del_repo():
    comando = dict(verificar.VERIFICACIONES)["pytest"]
    assert comando[1:3] == ["-m", "pytest"]
