# Diagramas de interacción (Entregable 2, tema 3.7)

Para cada funcionalidad clave hay un diagrama de secuencia (orden temporal) y un diagrama de colaboración
(organización de los objetos y mensajes numerados). Los dos describen la misma interacción.

> **Notación.** Las secuencias usan `sequenceDiagram` de Mermaid, que es UML. Mermaid no tiene diagrama de
> comunicación (colaboración) nativo: se dibuja con `flowchart` donde los nodos son objetos, los enlaces son
> las asociaciones y cada mensaje lleva su número de secuencia (`1`, `1.1`, `2`…), como pide la notación UML.

## 1. Ejecutar el pipeline con ingesta de la TRM (CU-02, CU-03)

### Secuencia

```mermaid
sequenceDiagram
    actor EV as Evaluador
    participant PL as Pipeline
    participant CB as CargadorBronze
    participant ET as ExtractorTrm
    participant SOC as API Socrata
    participant PG as PostgreSQL bronze
    participant LK as Lake Parquet
    participant DBT as dbt
    participant TB as Tablero

    EV->>PL: docker compose run --rm pipeline
    PL->>CB: ingesta TRM
    CB->>ET: extraer_trm()
    loop hasta agotar las páginas
        ET->>SOC: GET página
        alt responde bien
            SOC-->>ET: filas
        else falla
            ET->>ET: esperar (espera creciente)
            Note over ET,SOC: hasta 3 intentos, luego lanza ExtraccionError
        end
    end
    ET-->>CB: filas de la TRM
    CB->>LK: escribir_parquet(lote_id)
    CB->>PG: cargar_trm(filas, lote_id)
    CB-->>PL: código 0
    PL->>CB: ingesta IPC y tasa
    CB-->>PL: código 0
    PL->>DBT: dbt build
    DBT->>PG: construir silver y gold, ejecutar pruebas
    DBT-->>PL: código 0
    PL->>TB: crear tablero
    TB-->>PL: código 0
    PL-->>EV: Pipeline completo en N s
```

### Colaboración

```mermaid
flowchart LR
    EV([Evaluador]) -- "1: ejecutar pipeline" --> PL[Pipeline]
    PL -- "2: ingesta TRM" --> CB[CargadorBronze]
    CB -- "2.1: extraer_trm()" --> ET[ExtractorTrm]
    ET -- "2.1.1: GET página (hasta 3 intentos)" --> SOC[API Socrata]
    CB -- "2.2: escribir_parquet(lote_id)" --> LK[(Lake Parquet)]
    CB -- "2.3: cargar_trm(filas)" --> PG[(PostgreSQL)]
    PL -- "3: ingesta IPC y tasa" --> CB
    PL -- "4: dbt build" --> DBT[dbt]
    DBT -- "4.1: construir y probar" --> PG
    PL -- "5: crear tablero" --> TB[Tablero]
    PL -- "6: informar duración" --> EV
```

## 2. Consultar y descargar datos (CU-06)

### Secuencia

```mermaid
sequenceDiagram
    actor AN as Analista
    participant UI as Ui Streamlit
    participant CO as Consulta
    participant PG as PostgreSQL gold

    AN->>UI: elegir conjunto y rango
    UI->>CO: consultar(conexion, conjunto, desde, hasta)
    CO->>PG: SELECT con el rango
    PG-->>CO: columnas y filas
    CO-->>UI: columnas y filas
    alt hay filas
        UI-->>AN: vista previa
        AN->>UI: pedir descarga
        UI->>CO: a_csv(columnas, filas)
        CO-->>UI: texto CSV
        UI-->>AN: archivo CSV con exactamente esas filas
    else sin filas
        UI-->>AN: mensaje de que no hay datos (sin archivo)
    end
```

### Colaboración

```mermaid
flowchart LR
    AN([Analista]) -- "1: elegir conjunto y rango" --> UI[Ui Streamlit]
    UI -- "2: consultar(conjunto, desde, hasta)" --> CO[Consulta]
    CO -- "2.1: SELECT con el rango" --> PG[(PostgreSQL gold)]
    UI -- "3: mostrar vista previa o mensaje" --> AN
    AN -- "4: pedir descarga" --> UI
    UI -- "5: a_csv(columnas, filas)" --> CO
    UI -- "6: entregar el CSV" --> AN
```

## 3. Crear el tablero (CU-09)

### Secuencia

```mermaid
sequenceDiagram
    participant PL as Pipeline
    participant TB as Tablero
    participant CM as ClienteMetabase
    participant MB as API de Metabase

    PL->>TB: main()
    TB->>CM: iniciar_sesion(email, clave)
    CM->>MB: POST /session
    MB-->>CM: token
    TB->>CM: llamar GET /dashboard
    CM->>MB: GET /dashboard
    MB-->>TB: tableros existentes
    alt ya existe el tablero
        TB-->>PL: código 0 sin crear otro
    else no existe
        TB->>CM: registrar la base de datos (si falta)
        loop hasta 30 intentos
            TB->>MB: GET metadata de la base
            Note over TB,MB: espera a que sincronice gold.mart_mensual
        end
        TB->>MB: POST /card (3 tarjetas)
        TB->>MB: POST /dashboard y PUT dashcards
        TB-->>PL: código 0
    end
```

### Colaboración

```mermaid
flowchart LR
    PL[Pipeline] -- "1: main()" --> TB[Tablero]
    TB -- "2: iniciar_sesion()" --> CM[ClienteMetabase]
    CM -- "2.1: POST /session" --> MB[API de Metabase]
    TB -- "3: llamar GET /dashboard" --> CM
    TB -- "4: crear(cliente, env)" --> CM
    CM -- "4.1: registrar BD, tarjetas y tablero" --> MB
    TB -- "5: código de salida" --> PL
```

## Trazabilidad

| Interacción | CU | HU | RF/RNF | Prueba |
|---|---|---|---|---|
| 1. Pipeline con ingesta de la TRM | CU-02, CU-03 | HU-03, HU-06, HU-12 | RF-01, RF-02, RF-08 | CP-ING-01, 02, CP-E2E-01 |
| 2. Consultar y descargar | CU-06 | HU-14 | RF-09 | CP-APP-01 |
| 3. Crear el tablero | CU-09 | HU-13 | RF-07 | CP-DASH-01 |
