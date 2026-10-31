# Evidencia: instalación en máquina limpia (CP-INST-01, HU-02), 30 oct 2026

Clon nuevo del repositorio en un directorio temporal, `.env` copiado de `.env.example`
(solo se cambiaron los puertos para no chocar con el entorno de desarrollo), proyecto
Compose aparte y volúmenes eliminados antes de cada corrida (`docker compose down -v`).
Pasos del «Inicio rápido» del README.

## Defecto encontrado y corregido

Primera corrida: `docker compose run --rm pipeline` terminó con código 1 en la etapa
«tablero Metabase» (`Connection refused` a `metabase:3000`). Metabase no tenía healthcheck:
`up --wait` volvía al arrancar el contenedor, pero Metabase tarda ~35 s en inicializar.
Corrección en `docker-compose.yml`: healthcheck de Metabase (`/api/health`) y el servicio
`pipeline` depende de `metabase: service_healthy`.

## Corrida tras la corrección (desde cero)

```
$ docker compose up -d --wait        # postgres y metabase healthy
$ docker compose run --rm pipeline
==> ingesta TRM / ingesta IPC / ingesta tasa de intervención
==> dbt build
Done. PASS=43 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=43
==> tablero Metabase
Tablero creado: http://metabase:3000/dashboard/2
Pipeline completo en 18.4 s
```

Código de salida 0. Metabase respondió 200 en `/api/health` y la app web 200 en su puerto.
Resultado de CP-INST-01: **pasa**.
