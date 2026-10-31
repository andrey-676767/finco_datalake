# Entregable 2 — Análisis, Diseño UML y Especificación Técnica

**Proyecto:** Lakehouse analítico de datos financieros públicos (`finco_datalake`)
**Equipo:** David Restrepo · Juan Esteban · Andrey Machado
**Objetivo:** modelar la arquitectura, el comportamiento y la estructura del sistema.

Los modelos viven en `docs/` y se mantienen junto al código. Este índice los reúne y muestra cómo cubre cada
apartado del enunciado.

## Contenido

| Apartado del enunciado | Tema | Documento | Diagramas |
|---|---|---|---|
| Diagrama de casos de uso con plantilla de descripción | 3.5 | [casos-uso.md](../../docs/diseno/casos-uso.md) | 1 diagrama, 9 casos con plantilla |
| Diagrama de actividades de los flujos principales | 3.5 | [actividades.md](../../docs/diseno/actividades.md) | 4 diagramas |
| Diagrama de estado de la entidad crítica | 3.5 | [estados.md](../../docs/diseno/estados.md) | Ciclo de vida del lote |
| Diagrama de clases / modelo de dominio | 3.6 | [clases.md](../../docs/diseno/clases.md) | Dominio y clases de diseño |
| Diagrama de arquitectura de alto nivel | 3.6 | [arquitectura.md](../../docs/diseno/arquitectura.md) | Componentes, capas y despliegue, con justificación |
| Modelo de datos y ADR | 3.6 | [modelo-datos.md](../../docs/diseno/modelo-datos.md) | ER de las tres capas |
| Diagrama de secuencia de funcionalidades clave | 3.7 | [interaccion.md](../../docs/diseno/interaccion.md) | 3 secuencias |
| Diagrama de colaboración | 3.7 | [interaccion.md](../../docs/diseno/interaccion.md) | 3 colaboraciones |
| Plan preliminar de pruebas (unitarias e integración) | 2.5 | [plan-pruebas.md](../../docs/pruebas/plan-pruebas.md) | Estrategia, niveles y cobertura |
| Estrategia de versionado y gestión de cambios | 2.7 | [versionado.md](../../docs/gestion/versionado.md) | Modelo de ramas y flujo de cambios |

## Consistencia entre el diseño estático, el dinámico y el backlog

Cada fila une un caso de uso con su comportamiento (dinámico), su estructura (estático), su HU y su prueba.

| CU | HU | RF/RNF | Actividades | Estados | Clases | Interacción | Prueba |
|---|---|---|---|---|---|---|---|
| CU-01 Levantar el entorno | HU-01 | RNF-01 | — | — | Arquitectura (despliegue) | — | CP-INST-01 |
| CU-02 Ejecutar el pipeline | HU-12 | RF-08, RNF-02 | Diagrama 1 | — | Pipeline | Secuencia y colaboración 1 | CP-E2E-01, CP-PIPE-01 |
| CU-03 Cargar a bronze | HU-03 a HU-06 | RF-01, RF-02 | Diagrama 2 | Lote | Lote, CargadorBronze, ExtractorTrm | Secuencia y colaboración 1 | CP-ING-01, 02, 03 |
| CU-04 Construir silver y gold | HU-07 a HU-10 | RF-01b, RF-03 a RF-05 | Diagrama 4 | Lote (Transformado) | TRM, IPC, Tasa, hechos, mart | — | CP-SIL-01, 02, CP-GLD-01, 02 |
| CU-05 Consultar el tablero | HU-13 | RF-07 | — | Lote (Publicado) | Tablero, Visualizacion | — | CP-DASH-01 |
| CU-06 Consultar y descargar | HU-14 | RF-09 | Diagrama 3 | Lote (Publicado) | Consulta, Ui | Secuencia y colaboración 2 | CP-APP-01 |
| CU-07 Consultar el linaje | HU-11 | RF-06, RNF-05 | — | — | Dominio | — | CP-LIN-01 |
| CU-08 Instalar con el README | HU-02 | RNF-01, RF-08 | — | — | Arquitectura (despliegue) | — | CP-INST-01 |
| CU-09 Crear el tablero | HU-13 | RF-07 | Diagrama 1 | — | Tablero, ClienteMetabase | Secuencia y colaboración 3 | CP-DASH-01, CP-DASH-02 |

## Notas de notación

Los diagramas están escritos en Mermaid para que se rendericen en GitHub. Mermaid trae UML nativo para
**clases, estados y secuencia**. Para **casos de uso, actividades y colaboración** no existe un tipo nativo: se
dibujan con `flowchart` siguiendo la convención UML (actores, límite del sistema, `«include»`, nodos inicial y
final, decisiones, calles y mensajes numerados). Cada documento lo indica al inicio. Si el profesor exige
herramientas UML dedicadas, los modelos se pueden redibujar uno a uno con el mismo contenido.

## Pendientes

- Revisar entre los tres integrantes que los diagramas reflejen la implementación (criterio de consistencia).
- Confirmar con el profesor si la notación Mermaid es aceptable para casos de uso, actividades y colaboración.
