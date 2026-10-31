# 6. Product Backlog e historias de usuario

**Versión:** 1.1 — 25 de octubre de 2026
**Fuente:** historias HU-01 a HU-13 del README del repositorio (§8). Se conservan su redacción, prioridad y escenario original; el sprint y algunos responsables se reajustaron el 25 de octubre. HU-14 es nueva. Este documento añade la estimación, las dependencias, la prioridad MoSCoW y algunos escenarios adicionales (marcados como **propuesto**).

**Formato de criterios de aceptación.** Given-When-Then escrito en español con las palabras clave de Gherkin: `Dado` (Given), `Cuando` (When), `Entonces` (Then) e `Y` (And).

**Convenciones**

- **Prioridad:** Alta → Must · Media → Should (según el README).
- **Estimación:** puntos de historia en escala Fibonacci, con HU-06 (reintentos) como referencia de 2 puntos. Es una **propuesta** que el equipo debe validar en el planning (por ejemplo, con planning poker).
- **Estado:** todas las HU están en `Backlog` o `Ready` según el README v1.0. No se registra avance real.

---

## 1. Resumen del backlog

| ID | Épica | Historia (resumen) | Resp. | Sprint | Prioridad | Pts | Requisitos | Depende de |
|---|---|---|---|---|---|---|---|---|
| HU-01 | 1. Entorno | Levantar todo el entorno en Docker con un comando | Andrey | 2 | Alta (Must) | 3 | RNF-01 | — |
| HU-02 | 1. Entorno | Instalar y ejecutar siguiendo solo el README (solo Docker) | Andrey | Cierre | Alta (Must) | 3 | RNF-01, RF-08 | HU-12, HU-13, HU-14 |
| HU-03 | 2. Ingesta | Cargar la TRM histórica desde 2020 | David | 2 | Alta (Must) | 5 | RF-01, RF-02 | HU-01 |
| HU-04 | 2. Ingesta | Cargar el IPC mensual desde un CSV (desde 2019) | David | 2 | Alta (Must) | 3 | RF-01, RF-02 | HU-01 |
| HU-05 | 2. Ingesta | Cargar la tasa de intervención desde un CSV | David | 2 | Alta (Must) | 2 | RF-01, RF-02 | HU-01 |
| HU-06 | 2. Ingesta | Reintentos y registro de errores en la TRM | David | 3 | Media (Should) | 2 | RF-01 | HU-03 |
| HU-07 | 3. Silver | TRM limpia, por día calendario y sin duplicados | Juan | 3 | Alta (Must) | 3 | RF-03, RF-05 | HU-03 |
| HU-08 | 3. Silver | IPC por mes y tasa por vigencia | Juan | 3 | Alta (Must) | 5 | RF-03, RF-01b, RF-05 | HU-04, HU-05 |
| HU-09 | 4. Gold | Modelo estrella y mart mensual (Opción B) | Juan | 3 | Alta (Must) | 8 | RF-04, RF-01b | HU-07, HU-08 |
| HU-10 | 4. Gold | Pruebas de integridad referencial | David (apoyo) | 3 | Alta (Must) | 2 | RF-05 | HU-09 |
| HU-11 | 4. Gold | Consultar linaje de cada campo | Juan | 4 | Media (Should) | 3 | RF-06, RNF-05 | HU-09 |
| HU-12 | 5. Orquestación | Ejecutar todo el pipeline con un comando en Docker | Andrey | 3 | Alta (Must) | 3 | RF-08, RNF-02 | HU-03 a HU-05, HU-09 |
| HU-13 | 6. Visualización | Tablero ya cargado con TRM, inflación y tasa | Andrey | 4 | Alta (Must) | 5 | RF-07 | HU-09, HU-12 |
| HU-14 | 6. Visualización | Aplicación web para ver y descargar datos de gold | David | 4 | Media (Should) | 8 | RF-09 | HU-09 |
| | | **Total** | | | | **55** | | |

**Puntos por sprint:** sprint 2 = 13 · sprint 3 = 23 · sprint 4 = 16 · cierre = 3.

**Épica 7 (documentación y trazabilidad).** No son HU, son tareas del equipo:

| ID | Tarea | Responsable | Sprint |
|---|---|---|---|
| T-01 | Documento de requisitos RF/RNF | Todos | 1 |
| T-02 | Casos de uso y diagramas de flujo | David | 2 |
| T-03 | Diagrama de arquitectura / componentes | Andrey | 2 |
| T-04 | Modelo de datos (ER de las 3 capas) + ADR de la Opción B | Juan Esteban | 2 |
| T-05 | Matriz de trazabilidad v1 | Andrey | 3 |
| T-06 | Plan de pruebas y casos de prueba | Juan Esteban | 3 |
| T-07 | Ejecución de pruebas y evidencia | Todos (coordina Juan) | 4 |
| T-08 | Manual técnico y manual de usuario | Andrey | 4 |
| T-09 | Trazabilidad final, actas y retrospectiva general | Andrey (actas), todos (retro) | 4 |

## 2. Actores

| Actor | Descripción |
|---|---|
| Analista financiero | Usuario del tablero que consulta e interpreta los indicadores |
| Integrante del equipo | Desarrollador que construye y mantiene el pipeline |
| Evaluador | Profesor que instala y ejecuta el proyecto en su máquina |
| Product Owner | Prioriza el backlog y acepta las historias |

## 3. Historias de usuario

### Épica 1 — Configuración del entorno

#### HU-01 · Levantar el entorno con un comando

- **Como** integrante del equipo, **quiero** levantar PostgreSQL, Metabase, el pipeline y la aplicación web con un solo comando de Docker Compose, **para** que todos trabajemos sobre el mismo entorno.
- **Responsable:** Andrey · **Sprint:** 2 · **Prioridad:** Alta (Must) · **Estimación:** 3 pts · **Requisito:** RNF-01

```gherkin
Escenario: Levantar el entorno desde cero
  Dado que tengo Docker instalado y el repositorio clonado
  Y que copié .env.example a .env
  Cuando ejecuto "docker compose up -d"
  Entonces PostgreSQL acepta conexiones con los esquemas bronze, silver y gold creados
  Y Metabase responde en el puerto configurado
  Y el contenedor del pipeline y la aplicación web están disponibles
```

#### HU-02 · Instalar y ejecutar siguiendo solo el README

- **Como** evaluador, **quiero** instalar y ejecutar el proyecto en mi máquina siguiendo solo el README, **para** verificar su funcionamiento sin ayuda del equipo.
- **Responsable:** Andrey · **Sprint:** Cierre · **Prioridad:** Alta (Must) · **Estimación:** 3 pts · **Requisitos:** RNF-01, RF-08

```gherkin
Escenario: Instalación en una máquina limpia
  Dado una máquina con solo Docker instalado y sin datos previos del proyecto
  Cuando sigo los pasos del README en orden
  Entonces el pipeline termina sin errores
  Y puedo abrir el tablero con datos cargados y usar la aplicación web
```

### Épica 2 — Ingesta de datos

#### HU-03 · Cargar la TRM histórica

- **Como** analista financiero, **quiero** que la TRM histórica desde 2020 se cargue automáticamente desde datos.gov.co, **para** no descargarla a mano.
- **Responsable:** David · **Sprint:** 2 · **Prioridad:** Alta (Must) · **Estimación:** 5 pts · **Requisitos:** RF-01, RF-02

```gherkin
Escenario: Carga completa de la TRM
  Dado que la API Socrata de datos.gov.co está disponible
  Cuando ejecuto el extractor de TRM
  Entonces la tabla bronze de TRM contiene registros desde el 1 de enero de 2020
  Y cada registro tiene la fuente, la fecha y hora de carga y el identificador del lote
```

```gherkin
# Propuesto
Escenario: Nueva ejecución del extractor
  Dado que bronze ya contiene un lote de TRM
  Cuando ejecuto de nuevo el extractor de TRM
  Entonces se registra un lote nuevo con su propio identificador
  Y los registros de los lotes anteriores no se modifican
```

#### HU-04 · Cargar el IPC mensual

- **Como** analista financiero, **quiero** que el IPC mensual desde 2020 se cargue desde el Banco de la República, **para** analizar la inflación junto con la TRM.
- **Responsable:** David · **Sprint:** 2 · **Prioridad:** Alta (Must) · **Estimación:** 3 pts · **Requisitos:** RF-01, RF-02

```gherkin
Escenario: Carga del IPC
  Dado que el CSV de IPC exportado del Banco de la República (desde enero de 2019) está versionado en el repositorio
  Cuando ejecuto el cargador de IPC
  Entonces la tabla bronze de IPC contiene un registro por mes desde enero de 2020
  Y cada registro conserva el valor original sin transformar y sus metadatos de carga
```

#### HU-05 · Cargar la tasa de intervención

- **Como** analista financiero, **quiero** que las decisiones de tasa de intervención desde 2020 se carguen desde el Banco de la República, **para** relacionarlas con la inflación y la TRM.
- **Responsable:** David · **Sprint:** 2 · **Prioridad:** Alta (Must) · **Estimación:** 2 pts · **Requisitos:** RF-01, RF-02

```gherkin
Escenario: Carga de la tasa de intervención
  Dado que el CSV de tasa de intervención exportado del Banco de la República está versionado en el repositorio
  Cuando ejecuto el cargador de tasa de intervención
  Entonces la tabla bronze contiene cada cambio de tasa con su fecha de vigencia desde 2020
  Y cada registro tiene metadatos de origen y fecha de carga
```

#### HU-06 · Reintentos y registro de errores

- **Como** integrante del equipo, **quiero** que los extractores reintenten ante fallas de red y registren los errores, **para** que una caída temporal de la fuente no rompa el pipeline sin aviso.
- **Responsable:** David · **Sprint:** 3 · **Prioridad:** Media (Should) · **Estimación:** 2 pts · **Requisito:** RF-01

```gherkin
Escenario: Falla temporal de la fuente
  Dado que la fuente responde con error en el primer intento
  Cuando el extractor se ejecuta
  Entonces reintenta al menos 3 veces con espera creciente
  Y si todos los intentos fallan, registra el error en el log y termina con código distinto de 0
```

### Épica 3 — Transformación silver

#### HU-07 · TRM limpia y sin duplicados

- **Como** analista financiero, **quiero** la TRM limpia, tipada y sin duplicados, **para** confiar en los valores diarios.
- **Responsable:** Juan Esteban · **Sprint:** 3 · **Prioridad:** Alta (Must) · **Estimación:** 3 pts · **Requisitos:** RF-03, RF-05

```gherkin
Escenario: TRM sin duplicados
  Dado que bronze contiene la TRM cargada en dos lotes con fechas repetidas
  Cuando ejecuto "dbt build" sobre silver
  Entonces silver tiene un único registro por día calendario, con la vigencia original como columna
  Y gana el lote más reciente cuando una vigencia aparece en dos lotes
  Y los tests unique y not_null sobre la fecha pasan
```

#### HU-08 · IPC por mes y tasa por vigencia

- **Como** analista financiero, **quiero** el IPC por mes y la tasa de intervención por periodo de vigencia, **para** conocer qué tasa regía en cualquier fecha.
- **Responsable:** Juan Esteban · **Sprint:** 3 · **Prioridad:** Alta (Must) · **Estimación:** 5 pts · **Requisitos:** RF-03, RF-01b, RF-05

```gherkin
Escenario: Tasa de intervención por vigencia
  Dado que bronze contiene los cambios de tasa con su fecha de decisión
  Cuando ejecuto "dbt build" sobre silver
  Entonces cada registro tiene fecha_inicio y fecha_fin de vigencia
  Y los periodos de vigencia no se solapan
```

### Épica 4 — Modelado gold

#### HU-09 · Modelo estrella y mart mensual

- **Como** analista financiero, **quiero** un modelo estrella con hechos separados por periodicidad y un mart mensual, **para** comparar TRM, inflación y tasa en el mismo tablero (Opción B).
- **Responsable:** Juan Esteban · **Sprint:** 3 · **Prioridad:** Alta (Must) · **Estimación:** 8 pts · **Requisitos:** RF-04, RF-01b

```gherkin
Escenario: Mart mensual consolidado
  Dado que silver contiene TRM diaria, IPC mensual y tasa por vigencia
  Cuando ejecuto "dbt build" sobre gold
  Entonces existe una dimensión de fecha, un hecho diario de TRM y un hecho mensual de indicadores
  Y el mart mensual tiene una fila por mes con TRM promedio, IPC y tasa vigente
```

#### HU-10 · Integridad referencial

- **Como** integrante del equipo, **quiero** pruebas de integridad referencial entre hechos y dimensiones, **para** detectar datos huérfanos antes de que lleguen al tablero.
- **Responsable:** David (apoyo) · **Sprint:** 3 · **Prioridad:** Alta (Must) · **Estimación:** 2 pts · **Requisito:** RF-05

```gherkin
Escenario: Integridad referencial
  Dado que gold está construido
  Cuando ejecuto "dbt test"
  Entonces el test relationships entre cada hecho y la dimensión de fecha pasa
```

```gherkin
# Propuesto
Escenario: Detección de un dato huérfano
  Dado que un hecho contiene una fecha que no existe en la dimensión de fecha
  Cuando ejecuto "dbt test"
  Entonces el test relationships falla e identifica el registro huérfano
```

#### HU-11 · Linaje de datos

- **Como** analista financiero, **quiero** consultar de qué fuente y transformación sale cada campo del tablero, **para** justificar los números que reporto.
- **Responsable:** Juan Esteban · **Sprint:** 4 · **Prioridad:** Media (Should) · **Estimación:** 3 pts · **Requisitos:** RF-06, RNF-05

```gherkin
Escenario: Consultar el linaje
  Dado que ejecuté "dbt docs generate" y "dbt docs serve"
  Cuando abro el modelo del mart mensual en la documentación
  Entonces el grafo de linaje muestra el camino desde las tablas bronze hasta el mart
  Y cada columna del mart tiene una descripción que indica su origen
```

### Épica 5 — Orquestación

#### HU-12 · Pipeline de un solo comando

- **Como** evaluador, **quiero** ejecutar todo el pipeline con un solo comando, **para** reproducir los resultados sin conocer los detalles internos.
- **Responsable:** Andrey · **Sprint:** 3 · **Prioridad:** Alta (Must) · **Estimación:** 3 pts · **Requisitos:** RF-08, RNF-02

```gherkin
Escenario: Ejecución de punta a punta
  Dado que el entorno Docker está levantado
  Cuando ejecuto "docker compose run --rm pipeline"
  Entonces se ejecutan en orden la ingesta de las 2 fuentes y "dbt build"
  Y el script informa la duración total y termina con código 0 si todo fue exitoso
```

```gherkin
# Propuesto
Escenario: Falla en la ingesta
  Dado que un extractor termina con código distinto de 0
  Cuando ejecuto "docker compose run --rm pipeline"
  Entonces el pipeline no ejecuta "dbt build"
  Y termina con código distinto de 0 indicando qué etapa falló
```

### Épica 6 — Visualización y extracción

#### HU-13 · Tablero macroeconómico

- **Como** analista financiero, **quiero** un tablero con la evolución de la TRM, la inflación y la tasa de intervención, **para** analizar el comportamiento macroeconómico desde 2020.
- **Responsable:** Andrey · **Sprint:** 4 · **Prioridad:** Alta (Must) · **Estimación:** 5 pts · **Requisito:** RF-07

```gherkin
Escenario: Tablero macroeconómico
  Dado que gold contiene datos desde 2020
  Cuando abro el tablero en Metabase
  Entonces veo al menos 3 visualizaciones: evolución de la TRM, inflación anual y tasa de intervención frente a inflación
  Y puedo filtrar por rango de fechas
  Y el tablero fue creado automáticamente por un script contra la API de Metabase, sin pasos manuales
```

```gherkin
# Propuesto
Escenario: Filtro por rango de fechas
  Dado que el tablero muestra datos desde 2020
  Cuando selecciono un rango de fechas entre 2023-01-01 y 2023-12-31
  Entonces todas las visualizaciones muestran solo datos de ese rango
```

#### HU-14 · Aplicación web de consulta y extracción

- **Como** analista financiero, **quiero** una aplicación web donde visualizar los datos ya modelados y descargarlos filtrados, **para** usarlos en mi propio análisis sin acceder a la base de datos.
- **Responsable:** David · **Sprint:** 4 · **Prioridad:** Media (Should) · **Estimación:** 8 pts · **Requisito:** RF-09

```gherkin
Escenario: Descargar un conjunto de datos filtrado
  Dado que el entorno está levantado y gold contiene datos desde 2020
  Cuando abro la aplicación web y elijo el conjunto "mart mensual" y el rango entre 2023-01-01 y 2023-12-31
  Entonces veo una vista previa con solo los meses de 2023
  Y al pedir la descarga obtengo un archivo CSV con exactamente esas filas
```

```gherkin
# Propuesto
Escenario: Rango sin datos
  Dado que la aplicación web está abierta
  Cuando elijo un rango de fechas sin registros en gold
  Entonces la aplicación muestra un mensaje indicando que no hay datos
  Y no genera un archivo vacío
```

> **Pendiente de definir con el PO:** los conjuntos que ofrece la aplicación (se propone: TRM diaria, indicadores mensuales y mart mensual), los formatos de descarga (se propone solo CSV) y la tecnología.

## 4. Definition of Ready

Una HU puede entrar a un sprint si:

- [ ] Está escrita en formato "Como…, quiero…, para…".
- [ ] Tiene al menos un escenario Gherkin verificable.
- [ ] Está enlazada a al menos un requisito (RF o RNF).
- [ ] Tiene responsable y estimación.
- [ ] No depende de algo que aún no exista, o la dependencia está identificada.

## 5. Definition of Done

- [ ] Código en `main` mediante PR aprobado por otro integrante.
- [ ] `verificar.py` ejecutado sin errores y resultado pegado en el PR.
- [ ] Al menos una prueba asociada (pytest o test dbt), si aplica.
- [ ] Documentación actualizada.
- [ ] Criterios de aceptación Gherkin verificados por quien acepta la historia.
- [ ] Demostrable en la review del sprint.

**Regla de aprobación.** Las historias de David (ingesta) las acepta Juan o Andrey. Las historias de los demás las acepta David como PO. David no aprueba su propio trabajo.

## 6. Verificación del backlog frente a la DoR

| Criterio | HU-01 a HU-13 |
|---|---|
| Formato "Como… quiero… para…" | Cumple |
| Al menos un escenario Gherkin | Cumple |
| Enlazada a un requisito | Cumple |
| Responsable asignado | Cumple |
| Estimación | Propuesta en este documento, pendiente de validar por el equipo |
| Dependencias identificadas | Propuestas en la sección 1, pendientes de validar |

## 7. Observaciones para el planning

- **La capacidad exige ~10 h por semana por persona.** Con 5 h no caben los 55 puntos más la documentación (T-02 a T-09, actas, manuales). Con ~10 h hay unas 110 h. Si no se confirma esa dedicación, aplicar el orden de recorte (HU-14, HU-11, HU-06; lo decide el PO).
- **Picos de carga.** David tiene 10 puntos en el sprint 2 y Juan 16 en el sprint 3. Para aliviar, HU-10 pasa a David como apoyo (la acepta Andrey) y HU-11 pasa al sprint 4.
- **HU-09 es el cuello de botella.** Con 8 puntos, depende de HU-07 y HU-08, y de ella dependen HU-10, HU-11, HU-12, HU-13 y HU-14. Conviene empezar el ER (T-04) y el proyecto dbt en el sprint 2.
- **HU-02 depende de casi todo.** Solo se puede probar al final; por eso vive en la semana de cierre (16 – 20 nov). Conviene un ensayo parcial antes.
- **Reestimaciones.** HU-04 (5→3) y HU-05 (3→2) bajan porque ahora cargan un CSV versionado en el repositorio. Todas las estimaciones siguen pendientes de planning poker.
