"""Verificación local antes de abrir un PR (reemplaza a la integración continua).

Uso: python verificar.py

Corre ruff, pytest y `dbt build`; pega la salida en el PR. Ejecuta todas aunque una
falle y termina con código distinto de 0 si alguna falló. Requiere `.env` exportado y
PostgreSQL arriba (`docker compose up -d`).
"""

import subprocess
import sys

VERIFICACIONES = [
    ("ruff", ["ruff", "check", "ingesta/", "app/", "pipeline.py", "verificar.py"]),
    ("pytest", [sys.executable, "-m", "pytest", "ingesta", "app", "-q"]),
    ("dbt", ["dbt", "build", "--project-dir", "dbt", "--profiles-dir", "dbt"]),
]


def main(argv, correr=subprocess.run):
    if argv:
        print("uso: python verificar.py", file=sys.stderr)
        return 2
    fallaron = []
    for nombre, comando in VERIFICACIONES:
        print(f"==> {nombre}", flush=True)
        if correr(comando).returncode != 0:
            fallaron.append(nombre)
    if fallaron:
        print(f"Fallaron: {', '.join(fallaron)}", file=sys.stderr)
        return 1
    print("Todo en orden")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
