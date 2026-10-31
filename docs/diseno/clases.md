# Diagramas de clases (Entregable 2, tema 3.6)

Dos vistas: el modelo de dominio (qué existe en el negocio) y las clases de diseño (qué componentes lo
implementan). Los nombres de operaciones de la segunda vista son las funciones reales del código.

## 1. Modelo de dominio

```mermaid
classDiagram
    class Fuente {
        +String nombre
        +String tipo
        +String periodicidad
    }
    class Lote {
        +UUID loteId
        +DateTime cargadoEn
        +String archivo
        +String hashArchivo
    }
    class RegistroBronze {
        +int numeroFila
        +JSON fila
    }
    class TRM {
        +Date fecha
        +Decimal valor
    }
    class IPC {
        +Date mes
        +Decimal indice
    }
    class TasaIntervencion {
        +Date fechaInicio
        +Date fechaFin
        +Decimal tasa
    }
    class DimFecha {
        +Date fecha
        +int anio
        +int mes
        +int trimestre
        +Date anioMes
    }
    class HechoTrmDiaria {
        +Date fecha
        +Decimal valor
    }
    class HechoIndicadoresMensual {
        +Date anioMes
        +Decimal ipc
        +Decimal inflacionAnual
        +Decimal tasaVigente
    }
    class MartMensual {
        +Date anioMes
        +Decimal trmPromedio
        +Decimal ipc
        +Decimal inflacionAnual
        +Decimal tasaVigente
    }
    class Tablero {
        +String nombre
        +String filtroFechas
    }
    class Visualizacion {
        +String nombre
    }

    Fuente "1" --> "0..*" Lote : origina
    Lote "1" *-- "1..*" RegistroBronze : contiene
    RegistroBronze "0..*" ..> "1" TRM : se limpia en silver
    RegistroBronze "0..*" ..> "1" IPC : se limpia en silver
    RegistroBronze "0..*" ..> "1" TasaIntervencion : se limpia en silver
    DimFecha "1" o-- "0..*" HechoTrmDiaria : fecha
    DimFecha "1" o-- "0..*" HechoIndicadoresMensual : anioMes
    TRM "1" --> "1" HechoTrmDiaria
    IPC "1" --> "1" HechoIndicadoresMensual
    TasaIntervencion "1..*" --> "1" HechoIndicadoresMensual : vigente al cierre del mes
    HechoTrmDiaria "1..*" --> "1" MartMensual : promedio del mes
    HechoIndicadoresMensual "1" --> "1" MartMensual
    MartMensual "1" --> "0..*" Visualizacion : alimenta
    Tablero "1" *-- "3..*" Visualizacion
```

### Reglas del modelo

| Regla | Fuente |
|---|---|
| Un lote pertenece a una sola fuente y no se modifica | RF-02 |
| Cada fila de bronze conserva la fila original completa | RF-02 |
| Las vigencias de `TasaIntervencion` no se solapan | RF-01b, HU-08 |
| El mart tiene una fila por mes, desde 2020-01 | RF-01b, HU-09 |
| Un tablero tiene al menos 3 visualizaciones | RF-07 |

## 2. Clases de diseño

```mermaid
classDiagram
    class Pipeline {
        +ETAPAS
        +main(argv) int
    }
    class ExtractorTrm {
        <<modulo>>
        +extraer_trm(sesion, tam_pagina, espera) list
        -_pedir_pagina(sesion, params, espera)
    }
    class ExtraccionError {
        <<exception>>
    }
    class LectorCsv {
        <<modulo>>
        +leer_csv(ruta) tuple
    }
    class CargadorBronze {
        <<modulo>>
        +conectar()
        +crear_tablas(conn)
        +escribir_parquet(nombre, filas, lote_id, fuente, cargado_en)
        +cargar_trm(conn, filas)
        +cargar_csv(conn, conjunto, filas, meta)
        +main(argv) int
    }
    class Dbt {
        <<externa>>
        +build()
        +docs()
    }
    class ClienteMetabase {
        +url
        +iniciar_sesion(email, clave)
        +llamar(metodo, ruta, json)
    }
    class Tablero {
        <<modulo>>
        +definir_tarjetas(campo_fecha)
        +definir_paneles(ids)
        +crear(cliente, env)
        +main(argv) int
    }
    class Consulta {
        <<modulo>>
        +consultar(conexion, conjunto, desde, hasta)
        +a_csv(columnas, filas) str
    }
    class Ui {
        <<streamlit>>
    }
    class Verificar {
        +VERIFICACIONES
        +main(argv) int
    }

    Pipeline ..> CargadorBronze : etapas de ingesta
    Pipeline ..> Dbt : etapa dbt build
    Pipeline ..> Tablero : última etapa
    CargadorBronze ..> ExtractorTrm : TRM
    CargadorBronze ..> LectorCsv : IPC y tasa
    ExtractorTrm ..> ExtraccionError : lanza
    Tablero --> ClienteMetabase : usa
    Ui ..> Consulta : usa
    Verificar ..> Dbt : ejecuta build
```

### Responsabilidades

| Clase o módulo | Responsabilidad | Requisito |
|---|---|---|
| `Pipeline` | Ejecutar etapas en orden y detenerse en la primera que falle | RF-08 |
| `ExtractorTrm` | Paginar la API y reintentar al menos 3 veces | RF-01 |
| `LectorCsv` | Leer el CSV y calcular su hash | RF-01, RF-02 |
| `CargadorBronze` | Escribir Parquet y filas con metadatos de lote | RF-02 |
| `Tablero` y `ClienteMetabase` | Crear el tablero por la API sin pasos manuales | RF-07 |
| `Consulta` y `Ui` | Consultar gold y generar el CSV | RF-09 |
| `Verificar` | Ejecutar ruff, pytest y `dbt build` | RNF-03 |

## Trazabilidad

| Vista | CU | HU | RF/RNF |
|---|---|---|---|
| Dominio | CU-03 a CU-07 | HU-03 a HU-11 | RF-01 a RF-07 |
| Diseño | CU-02, CU-03, CU-06, CU-09 | HU-03 a HU-06, HU-12 a HU-14 | RF-01, RF-02, RF-07 a RF-09 |
