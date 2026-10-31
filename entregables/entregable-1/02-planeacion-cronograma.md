# 2. Planeación y cronograma

**Versión:** 1.1 — 25 de octubre de 2026
**Fuente de fechas y tareas:** `README.md` del repositorio (§4 fases, §12 checklist semanal, §13 ceremonias), **reajustadas el 25 de octubre de 2026** para cerrar en la fecha límite real: **20 de noviembre de 2026**.

> **Nota de estado.** El sprint 1 (21 sep – 25 oct) cerró sin repositorio funcional, entorno Docker ni código: solo existe la documentación de planeación y requisitos. El calendario original (4 sprints de 2 semanas, entrega final ~15 nov) ya no era alcanzable. Se comprimen los sprints 2 a 4 a una semana cada uno y se usa la semana 16 – 20 nov como colchón. **Los objetivos y el alcance no cambian**, salvo la historia nueva HU-14 (aplicación web de consulta y extracción), pedida por el PO el 25 de octubre.

---

## 1. Calendario por sprint

| Sprint | Fechas (2026) | Objetivo del sprint | Hito |
|---|---|---|---|
| 1 | 21 sep – 25 oct | Planeación y requisitos en borrador (documentos 00 a 06). **Cerrado sin entregables técnicos** | Acta del sprint 1 con el retraso como impedimento |
| 2 | 26 oct – 1 nov | Entregable 2 para la revisión intermedia (diseño UML, plan de pruebas y versionado, todo en el repositorio) y, en lo posible, Docker y bronze como avance del MVP | **Revisión intermedia: 30 oct (confirmada por el profesor)** |
| 3 | 2 – 8 nov | Silver y gold con pruebas dbt y pipeline completo en Docker | Cierre del sprint 3 |
| 4 | 9 – 15 nov | Tablero cargado con datos, aplicación web de consulta y extracción, pruebas ejecutadas y manuales | Cierre del sprint 4 |
| Cierre (colchón) | 16 – 20 nov | Instalación en máquina limpia, trazabilidad final, actas, retrospectiva y ensayo de demo | **Entrega final: 20 nov** |

> La revisión intermedia es el 30 de octubre y evalúa el Entregable 2 (análisis y diseño UML). El sprint 2 se reorienta a ese entregable.

## 2. Diagrama de Gantt

```mermaid
gantt
    title Cronograma finco_datalake (21 sep - 20 nov 2026), reajustado el 25 oct
    dateFormat YYYY-MM-DD
    axisFormat %d/%m
    excludes weekends

    section Sprint 1 - Planeacion (cerrado)
    Documentos de planeacion y requisitos 00-06 (Todos) :done, s1a, 2026-09-21, 2026-10-25
    Prueba de la API Socrata de TRM (David)             :done, s1b, 2026-10-24, 2026-10-25

    section Sprint 2 - Docker y bronze
    HU-01 Docker Compose (Andrey)                       :s2a, 2026-10-26, 2026-10-28
    verificar.py (Andrey)                               :s2b, 2026-10-28, 2026-10-30
    T-03 Arquitectura (Andrey)                          :s2c, 2026-10-29, 2026-11-01
    HU-03 Extractor TRM (David)                         :s2d, 2026-10-26, 2026-10-30
    HU-04 Cargador CSV de IPC (David)                   :s2e, 2026-10-29, 2026-11-01
    HU-05 Cargador CSV de tasa (David)                  :s2f, 2026-10-30, 2026-11-01
    T-02 Casos de uso y flujos (David)                  :s2g, 2026-10-26, 2026-11-08
    T-04 ER de 3 capas y ADR Opcion B (Juan)            :s2h, 2026-10-26, 2026-11-01
    Proyecto dbt y sources (Juan)                       :s2i, 2026-10-28, 2026-11-01
    Revision intermedia Entregable 2                    :milestone, m1, 2026-10-30, 0d

    section Sprint 3 - Silver, gold y pipeline
    HU-07 TRM en silver (Juan)                          :s3a, 2026-11-02, 2026-11-04
    HU-08 IPC y tasa en silver (Juan)                   :s3b, 2026-11-03, 2026-11-06
    HU-09 Modelo estrella y mart (Juan)                 :s3c, 2026-11-04, 2026-11-08
    T-06 Plan de pruebas (Juan)                         :s3d, 2026-11-02, 2026-11-06
    HU-06 Reintentos en TRM (David)                     :s3e, 2026-11-02, 2026-11-04
    HU-10 Integridad referencial, apoyo (David)         :s3f, 2026-11-06, 2026-11-08
    Aceptar HU de silver (David como PO)                :s3g, 2026-11-06, 2026-11-08
    pipeline v1 solo ingesta (Andrey)                   :s3h, 2026-11-02, 2026-11-04
    HU-12 Pipeline completo en Docker (Andrey)          :s3i, 2026-11-04, 2026-11-08
    T-05 Trazabilidad v1 (Andrey)                       :s3j, 2026-11-05, 2026-11-08
    Cierre sprint 3                                     :milestone, m2, 2026-11-08, 0d

    section Sprint 4 - Tablero, app web y pruebas
    HU-13 Tablero Metabase cargado por script (Andrey)  :s4a, 2026-11-09, 2026-11-13
    HU-14 Aplicacion web de consulta y extraccion (David) :s4b, 2026-11-09, 2026-11-15
    HU-11 Linaje con dbt docs (Juan)                    :s4c, 2026-11-09, 2026-11-11
    T-07 Pruebas de calidad y evidencia (Juan)          :s4d, 2026-11-10, 2026-11-15
    T-08 Manual tecnico y de usuario (Andrey)           :s4e, 2026-11-11, 2026-11-15
    Cierre sprint 4                                     :milestone, m3, 2026-11-15, 0d

    section Cierre - Colchon
    HU-02 Instalacion en maquina limpia (Andrey)        :s5a, 2026-11-16, 2026-11-18
    T-09 Trazabilidad final y actas (Andrey)            :s5b, 2026-11-16, 2026-11-19
    Retrospectiva general y trabajo futuro (Todos)      :s5c, 2026-11-17, 2026-11-19
    Ensayo de demo (Todos)                              :s5d, 2026-11-18, 2026-11-19
    Entrega final                                       :milestone, m4, 2026-11-20, 0d
```

## 3. Fases del ciclo de vida y sprints

| Fase | Sprint(s) | Responsable principal | Evidencia | Criterio de salida |
|---|---|---|---|---|
| 1. Planeación | 1 | Todos | Documentos 00 a 06, roles, calendario, GitHub Projects, acta del sprint 1 | Backlog con épicas y tablero visible para los 3 |
| 2. Requisitos | 1 – 2 | Todos (el PO prioriza) | Requisitos RF/RNF, HU con Gherkin, backlog priorizado | HU de los sprints 2 y 3 en estado "Ready" |
| 3. Análisis y diseño | 2 (ajustes en 3) | David: casos de uso · Juan: modelo de datos · Andrey: arquitectura | Casos de uso, flujos, arquitectura, ER, ADR | Diseño revisado por los 3 antes de iniciar silver |
| 4. Construcción | 2 – 4 | Cada uno su capa | Código en `main` vía PR | HU que cumplen la DoD |
| 5. Pruebas | 2 – 4 | Juan coordina | Plan de pruebas, casos y evidencia | Casos críticos ejecutados y documentados |
| 6. Despliegue | 4 y cierre | Andrey | `docker compose up -d` y `docker compose run --rm pipeline`, manual técnico | Instalación en máquina limpia aprobada (CP-INST-01) |
| 7. Cierre | Cierre | Todos | Manual de usuario, trazabilidad final, retrospectiva, trabajo futuro | Entrega final ensamblada y demo ensayada |

## 4. Ceremonias y seguimiento

| Ceremonia | Fecha | Duración | Responsable del acta |
|---|---|---|---|
| Review + retro sprint 1 / planning sprint 2 | 25 – 26 oct | 45 min | Andrey |
| Review + retro sprint 2 / planning sprint 3 | 1 – 2 nov | 45 min | Andrey |
| Review + retro sprint 3 / planning sprint 4 (coincide con el marcador de la revisión intermedia) | 8 – 9 nov | 45 min | Andrey |
| Review sprint 4 / planning del cierre | 15 – 16 nov | 45 min | Andrey |
| Review final + retrospectiva general | 19 – 20 nov | 60 min | Andrey |
| Daily asíncrona | Lunes, miércoles y viernes | Mensaje corto | Cada integrante |

**Tablero de seguimiento (GitHub Projects).**

- Columnas: Backlog → Ready → En progreso → En revisión → Hecho.
- Campos: Sprint (1-4 y Cierre), Épica (1-7), Responsable, Requisito (RF/RNF) y estimación.
- Etiquetas: `ingesta`, `dbt`, `infra`, `tablero`, `app`, `docs`, `bloqueado`.

## 5. Carga por integrante (puntos de historia)

Los puntos son una propuesta (ver `06-product-backlog.md`). HU-04 y HU-05 se reestimaron a la baja porque ahora cargan un CSV versionado en el repositorio. HU-14 es nueva.

| Integrante | Sprint 2 | Sprint 3 | Sprint 4 | Cierre | Total HU | Tareas de documentación (Épica 7) |
|---|---|---|---|---|---|---|
| David | 10 (HU-03, 04, 05) | 4 (HU-06, HU-10 de apoyo) | 8 (HU-14) | — | 22 | T-02 |
| Juan Esteban | — | 16 (HU-07, 08, 09) | 3 (HU-11) | — | 19 | T-04, T-06, T-07 |
| Andrey | 3 (HU-01) | 3 (HU-12) | 5 (HU-13) | 3 (HU-02) | 14 | T-03, T-05, T-08, T-09 |
| **Total** | **13** | **23** | **16** | **3** | **55** | |

**Lecturas del plan:**

- **Horas recomendadas: ~10 por semana por integrante** (~30 h/semana, unas 110 h entre el 26 oct y el 20 nov). Cálculo: 55 puntos a ~1,5 h por punto son ~80 h de construcción, y la documentación (T-02 a T-09, actas, manuales, pruebas con evidencia) suma ~30 h. Con 5 h por semana (~55 h) el plan no cabe. El equipo debe confirmar que puede dedicar ese tiempo.
- Con 10 h por semana los picos siguen altos: ~10 puntos de David en el sprint 2 y ~16 de Juan en el sprint 3 (unas 15 a 24 h para cada uno en una semana). Por eso el sprint 3 es el más riesgoso.
- HU-10 pasa de Juan a David como apoyo para aliviar el sprint 3; la acepta Andrey (nadie aprueba su propio trabajo).
- HU-11 pasa del sprint 3 al 4, y HU-06 del 2 al 3.
- Orden de recorte propuesto si el tiempo no alcanza (lo decide el PO): HU-14, HU-11, HU-06.

## 6. Riesgos de planeación

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| **Capacidad insuficiente:** 55 puntos más documentación en ~110 h (10 h por persona por semana) | Alta | Alto | Confirmar que el equipo dedica ~10 h por semana; usar el orden de recorte; alcance congelado salvo HU-14 |
| Inicio tardío: el sprint 1 cerró sin entregables técnicos | Ocurrido | Alto | Calendario comprimido, colchón del 16 al 20 nov, acta del sprint 1 con el retraso |
| **Revisión intermedia el 30 oct con el diseño UML sin hacer** | Alta | Alto | Priorizar el Entregable 2 en los 3 días restantes; el código de bronze pasa a segundo plano |
| HU-14 (aplicación web) agregada tarde, con 8 puntos | Alta | Medio | Primera en el orden de recorte; depende de HU-09 |
| IPC y tasa de intervención solo por descarga manual de CSV | Media | Medio | CSV versionados en el repositorio (aceptado por el profesor); URL directa como mejora futura |
| PO también es desarrollador | Alta | Medio | Regla de aprobación: nadie acepta sus propias historias |
| Tablero de Metabase no reproducible en la máquina del evaluador | Alta | Alto | Script que lo crea por la API de Metabase al final del pipeline; validar con CP-INST-01 |
| Sin CI, alguien fusiona código que rompe el pipeline | Media | Medio | `verificar.py` obligatorio con evidencia en el PR y `main` protegida |
| Curva de aprendizaje de dbt | Media | Medio | Juan prepara el proyecto dbt y las fuentes en el sprint 2 |
| Desbalance de carga | Alta | Medio | Reparto de HU-10 y HU-06 descrito arriba |
