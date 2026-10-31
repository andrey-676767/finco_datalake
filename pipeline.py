"""Pipeline de un solo comando (HU-12): ingesta de las fuentes y luego `dbt build`.

Uso: python pipeline.py

Las etapas corren en orden. Si una falla, el pipeline se detiene (no ejecuta las
siguientes, en particular `dbt build`), dice qué etapa falló y termina con el código
de salida de esa etapa.
"""

import subprocess
import sys
import time

ETAPAS = [
    ("ingesta TRM", [sys.executable, "-m", "ingesta.carga_bronze", "trm"]),
    ("ingesta IPC", [sys.executable, "-m", "ingesta.carga_bronze", "ipc"]),
    ("ingesta tasa de intervención", [sys.executable, "-m", "ingesta.carga_bronze", "tasa"]),
    ("dbt build", ["dbt", "build", "--project-dir", "dbt", "--profiles-dir", "dbt"]),
    ("tablero Metabase", [sys.executable, "-m", "metabase.tablero"]),
]


def main(argv, correr=subprocess.run, reloj=time.monotonic):
    if argv:
        print("uso: python pipeline.py", file=sys.stderr)
        return 2
    inicio = reloj()
    for nombre, comando in ETAPAS:
        print(f"==> {nombre}", flush=True)
        codigo = correr(comando).returncode
        if codigo != 0:
            print(f"error: falló la etapa «{nombre}» (código {codigo})", file=sys.stderr)
            return codigo
    print(f"Pipeline completo en {reloj() - inicio:.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
