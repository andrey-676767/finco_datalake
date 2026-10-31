# Plan de pruebas (T-06, Entregable 2 temas 2.5 y 2.7)

Las pruebas se ejecutan en local antes de cada PR con `python verificar.py` (ruff, pytest y `dbt build`); no hay integración continua (R-01).

## 1. Estrategia

**Principio.** Cada prueba nace de un requisito: RF/RNF → HU con criterios Given-When-Then → caso de prueba (CP).
La matriz está en `docs/gestion/trazabilidad.md`; un requisito sin caso de prueba se considera un defecto del plan.

### Niveles

| Nivel | Qué verifica | Herramienta | Entorno | Dónde corre |
|---|---|---|---|---|
| Unitario | Una función aislada, con dependencias simuladas (API, reloj, subprocesos) | pytest | Sin servicios | `pytest ingesta app` |
| Integración | Componentes reales entre sí: carga a PostgreSQL, transformaciones dbt, esquema y relaciones | pytest con PostgreSQL; `dbt build` | PostgreSQL de Compose | `pytest` y `dbt build` |
| Sistema (extremo a extremo) | El flujo completo en contenedores | `docker compose run --rm pipeline` | Docker | Manual o scripted |
| Aceptación | Los criterios Given-When-Then de la HU frente al sistema en marcha | Revisión guiada y consulta por API | Entorno completo | Manual |
| Instalación | Instalar y ejecutar siguiendo solo el README | Manual en clon limpio | Máquina con solo Docker | Manual |

### Criterios de entrada y salida

- **Entrada:** `.env` configurado y, para integración, PostgreSQL arriba (`docker compose up -d`). Si PostgreSQL no está disponible, las pruebas que lo requieren se omiten con aviso (no fallan en falso).
- **Salida para abrir un PR:** `python verificar.py` termina con «Todo en orden».
- **Salida de la entrega:** todos los CP pasan o quedan registrados con evidencia en `docs/pruebas/evidencia/`.

### Reglas de diseño de las pruebas

- Cada regla de un requisito tiene su prueba y cada prueba verifica el efecto observable: código de salida, mensajes y que una entrada rechazada no deje datos.
- Las pruebas usan la interfaz pública, no el almacenamiento interno.
- Las transformaciones dbt se prueban con pruebas de datos (`unique`, `not_null`, `relationships`) y con unit tests de dbt sobre entradas conocidas.
- Un defecto encontrado en una corrida real se reproduce primero en una prueba (por ejemplo, la prueba de humo de la app y el healthcheck de Metabase).

## 2. Casos de prueba derivados de requisitos

### Pruebas unitarias

| ID | Caso | Requisito | HU | Cómo se ejecuta | Estado |
|---|---|---|---|---|---|
| CP-ING-01 | El extractor TRM recorre todas las páginas de Socrata | RF-01 | HU-03 | `pytest ingesta` | Automatizada |
| CP-ING-02 | El extractor reintenta 3 veces y falla con código distinto de 0 | RF-01 | HU-06 | `pytest ingesta` | Automatizada |
| CP-APP-01 | La app descarga el CSV filtrado y avisa si no hay datos | RF-09 | HU-14 | `pytest app` | Automatizada; la interfaz responde en `:8501` |
| CP-PIPE-01 | El pipeline se detiene en la primera etapa que falla e informa cuál | RF-08 | HU-12 | `pytest ingesta` (`test_pipeline.py`) | Automatizada |
| CP-DASH-02 | El script del tablero define al menos 3 tarjetas y enlaza el filtro de fechas a cada una | RF-07 | HU-13 | `pytest ingesta` (`test_tablero.py`) | Automatizada |

### Pruebas de integración

| ID | Caso | Requisito | HU | Cómo se ejecuta | Estado |
|---|---|---|---|---|---|
| CP-ING-03 | Cada registro bronze tiene metadatos de origen y carga | RF-02 | HU-03, 04, 05 | `pytest ingesta` (requiere PostgreSQL) | Automatizada |
| CP-SIL-01 | TRM en silver única por fecha | RF-03, RF-05 | HU-07 | `dbt build` (test `unique`) | Automatizada |
| CP-SIL-02 | Vigencias de tasa sin solapamiento | RF-01b | HU-08 | `dbt build` (unit tests y `unique` en `silver_tasa_intervencion`) | Automatizada |
| CP-GLD-01 | Integridad referencial hechos → dim_fecha | RF-05 | HU-10 | `dbt build` (test `relationships`) | Automatizada |
| CP-GLD-02 | Mart mensual con una fila por mes desde 2020 | RF-01b, RF-04 | HU-09 | `dbt build` (`unique` y `not_null` sobre `anio_mes`) | Automatizada, incluido `dbt/tests/mart_mensual_empieza_en_2020_01.sql` |

### Pruebas de sistema, aceptación e instalación

| ID | Caso | Requisito | HU | Tipo | Estado |
|---|---|---|---|---|---|
| CP-E2E-01 | Pipeline completo termina con código 0 | RF-08, RNF-02 | HU-12 | Sistema | Ejecutada en Docker: código 0, `PASS=43 ERROR=0`, entre 12 y 18 s |
| CP-DASH-01 | Tablero muestra 3 visualizaciones con datos | RF-07 | HU-13 | Aceptación | Verificada por API: 3 tarjetas, 81 filas cada una, filtro `Fechas` |
| CP-LIN-01 | Cada columna del mart tiene descripción y el grafo llega a bronze | RF-06, RNF-05 | HU-11 | Aceptación | Manual con `dbt docs` |
| CP-INST-01 | Instalación en máquina limpia siguiendo el README | RNF-01, RF-08 | HU-02 | Instalación | Ejecutada el 30 oct en clon limpio: pasa (`docs/pruebas/evidencia/ejecucion-2026-10-30-instalacion-limpia.md`) |
| CP-CAL-01 | Estilo y calidad estática del código | RNF-03 | Todas | Estática | `ruff` dentro de `verificar.py` |

CP-APP-01, CP-PIPE-01, CP-DASH-02 y CP-LIN-01 se agregaron en este plan; no estaban en el README.

## 3. Cobertura requisito → prueba

| Requisito | Casos de prueba |
|---|---|
| RF-01 | CP-ING-01, CP-ING-02 |
| RF-01b | CP-SIL-02, CP-GLD-02 |
| RF-02 | CP-ING-03 |
| RF-03 | CP-SIL-01 |
| RF-04 | CP-GLD-02 |
| RF-05 | CP-SIL-01, CP-GLD-01 |
| RF-06 | CP-LIN-01 |
| RF-07 | CP-DASH-01, CP-DASH-02 |
| RF-08 | CP-E2E-01, CP-PIPE-01, CP-INST-01 |
| RF-09 | CP-APP-01 |
| RNF-01 | CP-INST-01 |
| RNF-02 | CP-E2E-01 (duración que informa el pipeline) |
| RNF-03 | CP-CAL-01 |
| RNF-04 | Historial de Git (ver `docs/gestion/versionado.md`) |
| RNF-05 | CP-LIN-01 |

## 4. Criterios de aceptación de la entrega

- `python verificar.py` termina con «Todo en orden».
- Todos los casos CP-* pasan o quedan registrados con su evidencia en T-07.

## 5. Evidencia (T-07)

Cada ejecución pega en el PR la salida de `verificar.py`. Los casos manuales guardan captura o registro en `docs/pruebas/evidencia/`.

Corridas registradas:

- `docs/pruebas/evidencia/ejecucion-2026-10-29.md` — por rama, antes del merge.
- `docs/pruebas/evidencia/ejecucion-2026-10-30-instalacion-limpia.md` — instalación en clon limpio (HU-02).
- `docs/pruebas/evidencia/ejecucion-2026-10-30.md` — sobre `main`: pipeline en Docker, datos cargados, tablero por API y app.
