# Entregable 1 — Planeación y requerimientos del proyecto

**Proyecto:** Lakehouse analítico de datos financieros públicos (`finco_datalake`)
**Repositorio:** https://github.com/andrey-676767/finco_datalake
**Equipo:** David Restrepo · Juan Esteban · Andrey Machado
**Versión:** 1.1 — 25 de octubre de 2026

---

## Contenido

| Archivo | Apartado del entregable | Criterio que cubre | Estado |
|---|---|---|---|
| [01-definicion-problema.md](01-definicion-problema.md) | Definición del problema, justificación, objetivos y alcance del MVP | Claridad y viabilidad del alcance (20%) | Completo. Contrastar con el documento base |
| [02-planeacion-cronograma.md](02-planeacion-cronograma.md) | Cronograma (Gantt), sprints, fases, ceremonias y carga | Coherencia del cronograma (20%) | Completo. Falta marcar el avance real |
| [03-metodologia.md](03-metodologia.md) | Comparativa de modelos y justificación de Scrum | Coherencia de la planificación (20%) | Completo |
| [04-elicitacion.md](04-elicitacion.md) | Informe de técnicas de elicitación | Correcta elicitación (30%) | **Parcial. Faltan resultados reales** |
| [05-requisitos.md](05-requisitos.md) | Matriz de requisitos funcionales y no funcionales | Correcta formulación de requisitos (30%) | Completo. Falta el umbral de RNF-02 |
| [06-product-backlog.md](06-product-backlog.md) | Product Backlog con historias de usuario y Given-When-Then | Estructura de HU y criterios (30%) | Completo. Estimaciones por validar |

## Cambios de la versión 1.1 (25 de octubre de 2026)

Decisiones tomadas por el PO tras revisar el estado real del proyecto:

1. **Calendario reajustado** a la fecha límite real (20 de noviembre). Sprints 2 a 4 de una semana y colchón del 16 al 20 de noviembre. Ver `02-planeacion-cronograma.md`.
2. **Arquitectura lakehouse híbrida** (decisión del PO del 27 oct, reemplaza a la de "data warehouse"): bronze se guarda como archivos Parquet inmutables por lote (el lake) y se replica en PostgreSQL; dbt construye silver y gold en PostgreSQL (el house). El profesor había aceptado "data warehouse o el nombre más adecuado".
3. **Todo corre en Docker.** El evaluador solo necesita Docker; dos comandos: `docker compose up -d` y `docker compose run --rm pipeline`.
4. **Tablero ya cargado con datos**, creado por un script contra la API de Metabase al final del pipeline.
5. **IPC y tasa de intervención** se cargan desde CSV descargados a mano y versionados en el repositorio. URL directa o cambio de fuente quedan como mejora futura. El IPC se carga desde enero de 2019 para calcular la inflación anual de 2020.
6. **TRM** se publica por vigencia: silver la expande a un registro por día calendario.
7. **HU-14 nueva:** aplicación web aparte para visualizar y descargar los datos de gold.
8. **RNF-02** queda en menos de 5 minutos (provisional).
9. **Elicitación:** T3 aplicada; T4 (entrevista al profesor) aplicada con respuestas por escrito.

## Qué viene del repositorio y qué se añadió

| Elemento | Origen |
|---|---|
| Calendario, sprints, roles, decisiones D-01 a D-08, riesgos, ceremonias | README del repositorio (se copian y se organizan) |
| IDs de requisitos (RF-01 a RF-08, RF-01b, RNF-01 a RNF-05) | README, matriz de trazabilidad (se completan con descripción, prioridad y verificación) |
| HU-01 a HU-13, su Gherkin, responsable y prioridad | README (el sprint y el responsable se reajustaron en la v1.1) |
| HU-14 (aplicación web de consulta y extracción) | **Añadida** el 25 de octubre por el PO |
| Diagrama de Gantt, comparativa de metodologías, informe de elicitación, estimaciones, dependencias, MoSCoW, escenarios Given-When-Then adicionales, restricciones | **Añadido** en estos documentos. Los escenarios adicionales están marcados como "Propuesto" |

## Pendientes antes de entregar

Estos puntos requieren información que no está en el repositorio. No los complete con suposiciones.

1. **Documento base.** El README remite a `plan-proyecto-lakehouse-financiero.md`, que no está en el repo. Hay que compararlo con `01-definicion-problema.md` y `05-requisitos.md` y corregir lo que difiera.
2. **Elicitación.** T4 está aplicada (falta la fecha de la entrevista). Faltan las fechas de las sesiones de decisión (T2), la paginación y el filtro desde 2020 de la API (T3) y, si se aplica, la encuesta (T5).
3. **Revisión intermedia (30 oct).** Confirmada. Evalúa el Entregable 2 (UML, plan de pruebas, versionado). Falta producir esos documentos en `docs/`.
4. **Capacidad del equipo.** Confirmar que cada integrante puede dedicar ~10 h por semana hasta el 20 de noviembre (con 5 h el backlog no cabe; ver `02-planeacion-cronograma.md`, sección 5).
5. **Estimaciones.** Validar los puntos en un planning poker (HU-04 y HU-05 reestimadas, HU-14 nueva).
6. **Escenarios propuestos.** Aceptar o descartar los marcados como "Propuesto" en el backlog.
7. **Supuestos del alcance.** Confirmar los elementos marcados como "Supuesto" en `01-definicion-problema.md` (sección 4.2).
8. **Repositorio.** El repositorio de trabajo es `DavidRestrepo66/finco_datalake_david` (donde David hace cambios propios). Falta decidir cómo se sincroniza con el repositorio del equipo (`andrey-676767/finco_datalake`).

## Cómo exportar a Word o PDF

Los archivos están en Markdown con tablas y un diagrama Mermaid. Con `pandoc` se pueden unir y convertir. El diagrama de Gantt hay que renderizarlo aparte (por ejemplo, en https://mermaid.live) y pegarlo como imagen en el documento final.

```bash
pandoc 0*.md -o entregable-1.docx
```
