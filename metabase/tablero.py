"""Crea el tablero macroeconómico en Metabase por su API (HU-13), sin pasos manuales.

Uso: python -m metabase.tablero

Configura Metabase la primera vez (usuario administrador y conexión a PostgreSQL),
crea tres preguntas sobre gold.mart_mensual y un tablero con filtro por rango de fechas.
Si el tablero ya existe, no hace nada. Lee el entorno: METABASE_URL, METABASE_ADMIN_EMAIL,
METABASE_ADMIN_PASSWORD y POSTGRES_*.
"""

import os
import sys
import time

import requests

NOMBRE_TABLERO = "Tablero macroeconómico"
NOMBRE_BD = "finco"
SQL_BASE = "select anio_mes, {columnas} from gold.mart_mensual [[where {{{{fechas}}}}]] order by anio_mes"


def _tarjeta(nombre, columnas, campo_fecha):
    return {
        "name": nombre,
        "display": "line",
        "visualization_settings": {
            "graph.dimensions": ["anio_mes"],
            "graph.metrics": [c.strip() for c in columnas.split(",")],
        },
        "dataset_query": {
            "type": "native",
            "native": {
                "query": SQL_BASE.format(columnas=columnas),
                "template-tags": {
                    "fechas": {
                        "id": "fechas",
                        "name": "fechas",
                        "display-name": "Fechas",
                        "type": "dimension",
                        "widget-type": "date/all-options",
                        "dimension": ["field", campo_fecha, None],
                    }
                },
            },
        },
    }


def definir_tarjetas(campo_fecha):
    return [
        _tarjeta("Evolución de la TRM (promedio mensual)", "trm_promedio", campo_fecha),
        _tarjeta("Inflación anual (%)", "inflacion_anual", campo_fecha),
        _tarjeta("Tasa de intervención frente a inflación (%)", "tasa_vigente, inflacion_anual", campo_fecha),
    ]


def definir_paneles(ids_tarjetas):
    return [
        {
            "id": -(i + 1),
            "card_id": card_id,
            "row": (i // 2) * 6,
            "col": (i % 2) * 12,
            "size_x": 12,
            "size_y": 6,
            "parameter_mappings": [
                {
                    "parameter_id": "fechas",
                    "card_id": card_id,
                    "target": ["dimension", ["template-tag", "fechas"]],
                }
            ],
        }
        for i, card_id in enumerate(ids_tarjetas)
    ]


class Cliente:
    def __init__(self, url, sesion=None):
        self.url = url.rstrip("/")
        self.http = sesion or requests.Session()

    def llamar(self, metodo, ruta, **kwargs):
        r = self.http.request(metodo, f"{self.url}/api{ruta}", timeout=60, **kwargs)
        r.raise_for_status()
        return r.json() if r.content else None

    def iniciar_sesion(self, correo, clave):
        r = self.http.post(f"{self.url}/api/session", json={"username": correo, "password": clave}, timeout=60)
        if not r.ok:
            props = self.llamar("GET", "/session/properties")
            r = self.http.post(f"{self.url}/api/setup", timeout=60, json={
                "token": props["setup-token"],
                "user": {"first_name": "Admin", "last_name": "Finco", "email": correo, "password": clave},
                "prefs": {"site_name": "Finco", "allow_tracking": False},
            })
            r.raise_for_status()
        self.http.headers["X-Metabase-Session"] = r.json()["id"]


def esperar_campo_fecha(cliente, id_bd, intentos=30):
    for _ in range(intentos):
        meta = cliente.llamar("GET", f"/database/{id_bd}/metadata")
        for tabla in meta.get("tables", []):
            if tabla["schema"] == "gold" and tabla["name"] == "mart_mensual":
                for campo in tabla["fields"]:
                    if campo["name"] == "anio_mes":
                        return campo["id"]
        time.sleep(2)
    raise RuntimeError("Metabase no sincronizó gold.mart_mensual: ¿corrió el pipeline (dbt build)?")


def crear(cliente, env):
    bds = cliente.llamar("GET", "/database")["data"]
    bd = next((b for b in bds if b["name"] == NOMBRE_BD), None)
    if bd is None:
        bd = cliente.llamar("POST", "/database", json={
            "engine": "postgres",
            "name": NOMBRE_BD,
            "details": {
                "host": env.get("METABASE_DB_HOST", "postgres"),
                "port": int(env.get("METABASE_DB_PORT", 5432)),
                "dbname": env["POSTGRES_DB"],
                "user": env["POSTGRES_USER"],
                "password": env["POSTGRES_PASSWORD"],
                "ssl": False,
            },
        })
    campo = esperar_campo_fecha(cliente, bd["id"])
    ids = []
    for t in definir_tarjetas(campo):
        t["dataset_query"]["database"] = bd["id"]
        ids.append(cliente.llamar("POST", "/card", json=t | {"database_id": bd["id"]})["id"])
    tablero = cliente.llamar("POST", "/dashboard", json={
        "name": NOMBRE_TABLERO,
        "parameters": [{"id": "fechas", "name": "Fechas", "slug": "fechas", "type": "date/all-options"}],
    })
    cliente.llamar("PUT", f"/dashboard/{tablero['id']}", json={"dashcards": definir_paneles(ids)})
    return tablero["id"]


def main(argv, env=os.environ, cliente=None):
    if argv:
        print("uso: python -m metabase.tablero", file=sys.stderr)
        return 2
    try:
        cliente = cliente or Cliente(env.get("METABASE_URL", "http://localhost:3000"))
        cliente.iniciar_sesion(env["METABASE_ADMIN_EMAIL"], env["METABASE_ADMIN_PASSWORD"])
        existentes = cliente.llamar("GET", "/dashboard")
        if any(d["name"] == NOMBRE_TABLERO for d in existentes):
            print(f"El tablero «{NOMBRE_TABLERO}» ya existe; no se crea otro.")
            return 0
        id_tablero = crear(cliente, env)
    except (KeyError, RuntimeError, requests.RequestException) as error:
        print(f"error: {error!r}", file=sys.stderr)
        return 1
    print(f"Tablero creado: {cliente.url}/dashboard/{id_tablero}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
