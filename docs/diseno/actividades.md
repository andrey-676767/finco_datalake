# Diagramas de actividades (Entregable 2, tema 3.5)

> **Notación.** Mermaid no tiene diagrama de actividades nativo. Se usa `flowchart` con la convención UML:
> `●` nodo inicial, `◉` nodo final, rombo para decisión o fusión, rectángulo redondeado para acción y `subgraph`
> como calle (partición) por responsable. Las guardas van entre corchetes en las flechas.

## 1. Ejecutar el pipeline (CU-02, HU-12, RF-08)

Fuente en código: `pipeline.py` (`ETAPAS`). Si una etapa falla, las siguientes no se ejecutan.

```mermaid
flowchart TD
    I((●)) --> A

    subgraph EV[Evaluador]
        A(Ejecutar docker compose run --rm pipeline)
    end

    subgraph PL[Pipeline]
        B(Ingesta TRM)
        C(Ingesta IPC)
        D(Ingesta tasa de intervención)
        E(dbt build)
        F(Crear tablero en Metabase)
        G(Informar duración total)
        H(Informar etapa fallida)
        D1{¿código 0?}
        D2{¿código 0?}
        D3{¿código 0?}
        D4{¿código 0?}
        D5{¿código 0?}
    end

    A --> B --> D1
    D1 -- "[sí]" --> C --> D2
    D2 -- "[sí]" --> D --> D3
    D3 -- "[sí]" --> E --> D4
    D4 -- "[sí]" --> F --> D5
    D5 -- "[sí]" --> G --> OK((◉ código 0))
    D1 -- "[no]" --> H
    D2 -- "[no]" --> H
    D3 -- "[no]" --> H
    D4 -- "[no]" --> H
    D5 -- "[no]" --> H
    H --> KO((◉ código distinto de 0))
```

## 2. Cargar una fuente a bronze (CU-03, HU-03 a HU-06, RF-01, RF-02)

Dos caminos de lectura según la fuente; ambos convergen en la escritura de un lote.

```mermaid
flowchart TD
    I((●)) --> T{¿Qué fuente?}

    subgraph SOC[Camino TRM]
        P(Pedir página a la API Socrata)
        R{¿respondió bien?}
        N{¿intentos menores a 3?}
        W(Esperar con espera creciente)
        M{¿hay más páginas?}
    end

    subgraph CSV[Camino IPC o tasa]
        L(Leer el CSV y calcular su hash)
        V{¿existe y tiene filas?}
    end

    subgraph LOTE[Escritura del lote]
        G(Generar lote_id y cargado_en)
        PQ(Escribir Parquet inmutable del lote)
        PG(Insertar filas en bronze.*_raw)
    end

    T -- "[TRM]" --> P --> R
    R -- "[no]" --> N
    N -- "[sí]" --> W --> P
    N -- "[no]" --> LOGERR(Registrar el error en el log)
    R -- "[sí]" --> M
    M -- "[sí]" --> P
    M -- "[no]" --> G
    T -- "[IPC o tasa]" --> L --> V
    V -- "[sí]" --> G
    V -- "[no]" --> ERR(Informar el error)
    G --> PQ --> PG --> OK((◉ lote creado))
    LOGERR --> KO((◉ código distinto de 0))
    ERR --> KO
```

## 3. Consultar y descargar datos (CU-06, HU-14, RF-09)

```mermaid
flowchart TD
    I((●)) --> A

    subgraph AN[Analista]
        A(Elegir conjunto y rango de fechas)
        Z(Descargar el CSV)
    end

    subgraph AP[Aplicación web]
        Q(Consultar gold con el rango)
        D{¿hay filas?}
        PV(Mostrar vista previa)
        MSG(Mostrar mensaje de que no hay datos)
        CSV(Generar CSV con exactamente esas filas)
    end

    A --> Q --> D
    D -- "[sí]" --> PV --> Z --> CSV --> OK((◉))
    D -- "[no]" --> MSG --> OK2((◉ sin archivo))
```

## 4. Construir silver y gold (CU-04, HU-07 a HU-10)

```mermaid
flowchart TD
    I((●)) --> S1

    subgraph SIL[Silver]
        S1(TRM: un registro por día, gana el lote más reciente)
        S2(IPC: un registro por mes desde 2019)
        S3(Tasa: fecha_inicio y fecha_fin sin solapes)
    end

    subgraph GLD[Gold]
        G1(dim_fecha)
        G2(fact_trm_diaria)
        G3(fact_indicadores_mensual)
        G4(mart_mensual)
    end

    T{¿pasan las pruebas de calidad?}

    S1 --> F1[" "]
    S2 --> F1
    S3 --> F1
    F1 --> G1
    G1 --> G2
    G1 --> G3
    G2 --> G4
    G3 --> G4
    G4 --> T
    T -- "[sí]" --> OK((◉ build exitoso))
    T -- "[no]" --> KO((◉ build falla e identifica el registro))
```

Las flechas desde silver hacia `F1` y desde `G1` hacia `G2` y `G3` representan sincronización (barra de
bifurcación y unión) en la notación UML: las tres tablas de silver deben estar listas antes de gold, y los dos
hechos se construyen en paralelo antes del mart.

## Trazabilidad

| Diagrama | CU | HU | RF/RNF | Prueba |
|---|---|---|---|---|
| 1. Ejecutar el pipeline | CU-02 | HU-12 | RF-08, RNF-02 | CP-E2E-01 |
| 2. Cargar una fuente | CU-03 | HU-03 a HU-06 | RF-01, RF-02 | CP-ING-01, 02, 03 |
| 3. Consultar y descargar | CU-06 | HU-14 | RF-09 | CP-APP-01 |
| 4. Construir silver y gold | CU-04 | HU-07 a HU-10 | RF-01b, RF-03 a RF-05 | CP-SIL-01, 02, CP-GLD-01, 02 |
