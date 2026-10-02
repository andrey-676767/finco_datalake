# Plan de Ciclo de Vida del Software — Lakehouse Analítico de Datos Financieros Públicos

**Materia:** Ingeniería de Software — Universidad Católica Luis Amigó
**Metodología:** Scrum (4 sprints de 2 semanas)
**Equipo:** David Restrepo (PO + ingesta), Juan Esteban (modelos dbt), Andrey Machado (Docker / orquestación / Metabase)
**Documento base:** `plan-proyecto-lakehouse-financiero.md` (fuente de verdad del alcance)
**Versión:** 1.0 — 1 de octubre de 2026

---

## 0. Cómo usar este documento

Este archivo es el **plan operativo** del proyecto: dice qué se hace en cada fase del ciclo de vida, en qué sprint, quién lo hace y qué artefacto queda como evidencia. El documento base sigue siendo la fuente de verdad del **alcance**; este documento lo aterriza en fechas, tareas y plantillas.

| Sección | Para qué sirve |
|---|---|
| 1 | Decisiones ya tomadas y cambios respecto al documento base |
| 2 | Calendario real con fechas |
| 3 | Plan de recuperación (el proyecto va en la semana 2 sin nada construido) |
| 4 | Fases del ciclo de vida mapeadas a sprints |
| 5 | Roles, responsabilidades y regla de aprobación |
| 6 | Gestión de configuración: repositorio, ramas, commits, PR |
| 7 | Calidad sin CI: verificación local, DoR y DoD |
| 8 | Backlog inicial con historias de usuario (Gherkin) |
| 9 | Casos de uso |
| 10 | Plan de pruebas |
| 11 | Matriz de trazabilidad base |
| 12 | Checklist semanal por integrante |
| 13 | Ceremonias Scrum con fechas |
| 14 | Riesgos actualizados |
| 15 | Plantillas de artefactos |
| 16 | Próximos pasos (próximas 72 horas) |

---

## 1. Decisiones base

### 1.1 Decisiones vigentes

| # | Decisión | Estado |
|---|---|---|
| D-01 | Indicadores: TRM (diaria), IPC (mensual) y tasa de intervención (por decisión de la Junta) | Confirmada |
| D-02 | Histórico desde enero de 2020 | Confirmada |
| D-03 | Periodicidad mixta: **Opción B** — hechos separados; tasa de intervención modelada por vigencia (fecha inicio / fecha fin); mart mensual en gold | Confirmada (falta documentarla como ADR, ver 15.7) |
| D-04 | PostgreSQL con esquemas `bronze`, `silver`, `gold`; dbt Core; script Python de orquestación; Metabase | Confirmada |
| D-05 | El evaluador debe poder ejecutar todo el proyecto en su propia máquina | Confirmada (impacta RNF-01, RF-08 y manual técnico) |
| D-06 | Cada integrante sustenta su propia parte | Confirmada |
| D-07 | **Sin integración continua**: las pruebas se ejecutan localmente antes de cada PR | Confirmada |
| D-08 | Estrategia de ramas: GitHub Flow simplificado (ver sección 6) | Recomendada en este documento |

### 1.2 Cambios respecto al documento base

> Estos puntos **contradicen** el documento base y deben corregirse allí para que no haya dos versiones distintas en la entrega.

| Sección del documento base | Dice | Ahora es | Acción |
|---|---|---|---|
| 5. Stakeholders | Product Owner = profesor; David = representante del PO | **David es el Product Owner**; el profesor es evaluador (stakeholder externo) | Actualizar la tabla de stakeholders y la sección 6 ("validada por el PO") |
| 11. Cronograma | Semanas sin fechas | Semana 1 inició el 21 de septiembre de 2026 (ver sección 2) | Agregar fechas al cronograma |
| 11. Cronograma | Sprint 1 con requisitos, HU y Docker terminados | Sprint 1 cierra sin esos entregables; se aplica el plan de recuperación (sección 3) | Registrarlo en el acta del sprint 1 como impedimento |

**Consecuencia del cambio de PO:** David es a la vez Product Owner y desarrollador de la ingesta. Para evitar que apruebe su propio trabajo se aplica la **regla de aprobación** de la sección 5.2.

---

## 2. Calendario real

| Sprint | Semana | Fechas | Hito |
|---|---|---|---|
| 1 | 1 | 21 – 27 sep | — |
| 1 | 2 | 28 sep – 4 oct | Cierre sprint 1 (**semana actual**) |
| 2 | 3 | 5 – 11 oct | — |
| 2 | 4 | 12 – 18 oct | **ENTREGA DE MITAD (~18 oct)** |
| 3 | 5 | 19 – 25 oct | — |
| 3 | 6 | 26 oct – 1 nov | Cierre sprint 3 |
| 4 | 7 | 2 – 8 nov | — |
| 4 | 8 | 9 – 15 nov | **ENTREGA FINAL (~15 nov)** |

> Confirmar con el profesor las fechas exactas de las dos entregas y ajustar esta tabla si difieren.

---

## 3. Plan de recuperación (semana 2 sin nada construido)

**Situación:** el sprint 1 cierra el 4 de octubre y no hay requisitos, historias de usuario, repositorio ni entorno Docker. La entrega de mitad está a ~2,5 semanas.

**Lo que exige la entrega de mitad** (documento base, sección 12): requisitos, HU, casos de uso, diagramas de flujo y arquitectura, backlog priorizado, actas de sprints 1-2 y prototipo con Docker + ingesta de las 2 fuentes en bronze.

**Estrategia:**

1. **Lo mínimo para cerrar el sprint 1 (antes del lunes 5 oct):**
   - Repositorio creado con la estructura de la sección 6.1 y GitHub Projects con las 7 épicas.
   - Requisitos de la sección 13 del documento base revisados y numerados (pueden quedar en borrador).
   - Historias de usuario de la sección 8 revisadas por el PO (David) y por un segundo integrante.
   - Prueba rápida de la API Socrata (TRM) y del formato de descarga del Banco de la República.
2. **Todo lo demás del sprint 1 pasa al sprint 2**, que queda más cargado. Para compensar:
   - Docker Compose (Andrey) se hace en la semana 3, **antes** de que la ingesta lo necesite.
   - La documentación de diseño (ER, flujos, arquitectura) se hace en paralelo al código, no después.
   - Las pruebas de ingesta se escriben junto con cada extractor, no al final.
3. **Si en la semana 3 el formato del Banco de la República sigue sin resolverse**, se entrega la mitad con TRM completa en bronze y las fuentes del Banco con extractor parcial documentado como impedimento. Esto es una contingencia, no el plan.

**El acta del sprint 1 debe registrar el retraso como impedimento** y la decisión de mover las tareas; eso es evidencia legítima de gestión Scrum, no algo que haya que ocultar.

---

## 4. Fases del ciclo de vida mapeadas a sprints

El proyecto sigue Scrum, así que las fases no son secuenciales en cascada: se solapan entre sprints. La tabla indica dónde se concentra cada una.

| Fase | Sprint(s) | Responsable principal | Artefactos (evidencia) | Criterio de salida |
|---|---|---|---|---|
| 1. Planeación | 1 | Todos | Este documento, roles, calendario, GitHub Projects, acta sprint 1 | Backlog creado con épicas y tablero visible para los 3 |
| 2. Requisitos | 1 – 2 | Todos (PO prioriza) | Documento de requisitos (RF/RNF), HU con Gherkin, backlog priorizado | HU de sprints 2 y 3 en estado "Ready" (sección 7.2) |
| 3. Análisis y diseño | 2 (ajustes en 3) | David: casos de uso y flujos · Juan: modelo de datos · Andrey: arquitectura | Casos de uso, diagramas de flujo, diagrama de arquitectura/componentes, ER bronze/silver/gold, ADR de periodicidad (Opción B) | Diseño revisado por los 3 antes de iniciar silver |
| 4. Construcción | 2 – 4 | Cada uno su capa | Código en `main` vía PR: extractores, modelos dbt, pipeline, tablero | HU cumplen la DoD (sección 7.3) |
| 5. Pruebas | 2 – 4 | Juan coordina; cada uno prueba su capa | Plan de pruebas, casos de prueba, evidencia de ejecución (capturas/logs) | Todos los casos críticos ejecutados y resultados documentados |
| 6. Despliegue / instalación | 4 | Andrey | `docker compose up` + comando único de pipeline, README, manual técnico | Prueba de instalación en máquina limpia aprobada (CP-INST-01) |
| 7. Cierre y mantenimiento | 4 | Todos | Manual de usuario, trazabilidad final, retrospectiva general, sección "trabajo futuro" | Entrega final ensamblada y ensayo de demo realizado |

### 4.1 Objetivo de cada sprint

| Sprint | Objetivo del sprint |
|---|---|
| 1 | Tener el proyecto organizado: repositorio, backlog, requisitos y HU en borrador, fuentes verificadas |
| 2 | Tener el entorno Docker funcionando y los datos de las 2 fuentes cargados en bronze, con el diseño documentado (**entrega de mitad**) |
| 3 | Tener los datos limpios en silver y modelados en gold, con pruebas dbt y pipeline de un solo comando |
| 4 | Tener el tablero funcionando, las pruebas ejecutadas, los manuales escritos y el proyecto instalable en la máquina del evaluador (**entrega final**) |

---

## 5. Roles y responsabilidades

### 5.1 Roles

| Persona | Rol Scrum | Desarrollo | Documentación a cargo |
|---|---|---|---|
| **David Restrepo** | Product Owner + Developer | Ingesta en Python de las 2 fuentes (bronze) | Casos de uso, diagramas de flujo, priorización del backlog |
| **Juan Esteban** | Developer | Modelos dbt (silver y gold) y pruebas de calidad | Plan y casos de prueba, modelo de datos (ER), ADR de periodicidad |
| **Andrey Machado** | Scrum Master + Developer | Docker, orquestación, Metabase | Arquitectura, manual técnico y de usuario, matriz de trazabilidad, actas |
| **Profesor** | Evaluador (stakeholder externo) | — | Recibe entregas y ejecuta el proyecto en su máquina |

> Asignación de Scrum Master: el documento base la pone en el integrante C (Docker/orquestación/Metabase), que corresponde a Andrey. Si el equipo decide otra cosa, actualizar aquí y en el documento base.

### 5.2 Regla de aprobación (por ser David PO y developer)

- **Historias de otros integrantes:** las acepta David como PO en la review.
- **Historias de David (ingesta):** las acepta **otro integrante** (Juan o Andrey) verificando los criterios de aceptación Gherkin; David no se autoaprueba.
- **Todo PR** requiere la revisión de al menos una persona distinta de su autor (alineado con la DoD).

---

## 6. Gestión de configuración

### 6.1 Estructura del repositorio

```
lakehouse-financiero/
├── README.md                  # Cómo levantar y ejecutar todo (para el evaluador)
├── docker-compose.yml         # PostgreSQL + Metabase (+ contenedor de ingesta/dbt si aplica)
├── .env.example               # Variables de entorno sin secretos reales
├── pipeline.py                # Comando único: ingesta → dbt build (RF-08)
├── verificar.py               # Verificación local antes de cada PR (sección 7.1)
├── ingesta/
│   ├── extractores/
│   │   ├── trm_socrata.py
│   │   └── banrep.py          # IPC y tasa de intervención
│   ├── carga_bronze.py
│   └── tests/                 # pytest
├── dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── silver/
│   │   └── gold/
│   └── tests/
├── metabase/                  # Respaldo/instrucciones del tablero
└── docs/
    ├── requisitos.md
    ├── historias-usuario.md
    ├── casos-uso.md
    ├── diagramas/             # Mermaid o imágenes exportadas
    ├── adr/                   # Registros de decisiones de arquitectura
    ├── actas/                 # sprint-1.md ... sprint-4.md
    ├── pruebas/               # plan, casos y evidencia
    ├── trazabilidad.md
    └── manuales/
```

### 6.2 Estrategia de ramas recomendada: GitHub Flow simplificado

Se recomienda este modelo porque es el más simple que todavía cumple la DoD ("revisada por al menos otro integrante") y genera trazabilidad automática. Git Flow (ramas `develop`, `release`, `hotfix`) es excesivo para 3 personas y 8 semanas.

1. `main` siempre funciona y está **protegida**: no se permite push directo; todo entra por Pull Request con 1 aprobación.
2. Cada historia tiene su rama corta, creada desde `main`:
   - `feature/HU-03-extractor-trm`
   - `fix/HU-03-paginacion-trm`
   - `docs/casos-de-uso`
3. Ramas de vida corta (idealmente menos de una semana) para evitar conflictos grandes.
4. Antes de abrir el PR: `git pull origin main`, resolver conflictos y correr `python verificar.py`.
5. El PR se enlaza al issue con `Closes #<número>`: así GitHub Projects mueve la tarjeta y queda la traza HU → código.
6. Fusionar con **squash merge** para que cada historia quede como un commit limpio en `main`.

### 6.3 Convención de commits

Formato: `tipo(alcance): descripción breve (HU-xx)`

| Tipo | Uso | Ejemplo |
|---|---|---|
| `feat` | Funcionalidad nueva | `feat(ingesta): extractor TRM con paginación (HU-03)` |
| `fix` | Corrección | `fix(silver): deduplicar TRM por fecha (HU-07)` |
| `test` | Pruebas | `test(ingesta): mock de respuesta Socrata (HU-03)` |
| `docs` | Documentación | `docs(diseño): ER de las tres capas` |
| `chore` | Configuración | `chore(docker): servicio de Metabase` |

### 6.4 Tablero de GitHub Projects

- **Columnas:** Backlog → Ready → En progreso → En revisión → Hecho.
- **Campos personalizados:** Sprint (1-4), Épica (1-7), Responsable, Requisito (RF/RNF), Puntos o estimación en horas.
- **Etiquetas:** `ingesta`, `dbt`, `infra`, `tablero`, `docs`, `bloqueado`.

---

## 7. Calidad sin integración continua

### 7.1 Verificación local obligatoria antes de cada PR

Como no hay CI, `verificar.py` reemplaza esa función: cada autor lo ejecuta y pega el resultado en el PR.

| Paso | Comando sugerido | Aplica a |
|---|---|---|
| Estilo Python (PEP8, RNF-03) | `ruff check ingesta/` | Ingesta, orquestación |
| Pruebas unitarias | `pytest ingesta/tests` | Ingesta |
| Modelos y pruebas dbt | `dbt build` (desde `dbt/`) | Silver, gold |
| Estilo SQL (opcional) | `sqlfluff lint dbt/models` | Silver, gold |

El script debe terminar con código de salida distinto de 0 si algo falla, para que sea evidente.

### 7.2 Definition of Ready (una HU puede entrar a un sprint si…)

- [ ] Está escrita en formato "Como…, quiero…, para…".
- [ ] Tiene al menos un escenario Gherkin verificable.
- [ ] Está enlazada a al menos un requisito (RF o RNF).
- [ ] Tiene responsable y estimación.
- [ ] No depende de algo que aún no exista (o la dependencia está identificada).

### 7.3 Definition of Done (documento base, sección 7, con precisiones)

- [ ] Código en `main` mediante PR aprobado por otro integrante.
- [ ] `verificar.py` ejecutado sin errores y resultado pegado en el PR.
- [ ] Al menos una prueba asociada (pytest o test dbt), si aplica.
- [ ] Documentación actualizada (modelo dbt documentado o sección del documento correspondiente).
- [ ] Criterios de aceptación Gherkin verificados por quien acepta la historia (sección 5.2).
- [ ] Demostrable en la review del sprint.

---

## 8. Backlog inicial con historias de usuario

> Borrador para revisión del PO. Prioridad: **Alta** = necesaria para la entrega de mitad o bloquea a otros; **Media** = necesaria para la entrega final; **Baja** = deseable.

**Actores:** analista financiero (usuario del tablero), integrante del equipo (desarrollador), evaluador (ejecuta el proyecto en su máquina), Product Owner.

### Épica 1 — Configuración del entorno

**HU-01** · Andrey · Sprint 2 · Prioridad Alta · RNF-01
Como integrante del equipo, quiero levantar PostgreSQL y Metabase con un solo comando de Docker Compose, para trabajar todos sobre el mismo entorno.

```gherkin
Escenario: Levantar el entorno desde cero
  Dado que tengo Docker instalado y el repositorio clonado
  Y que copié .env.example a .env
  Cuando ejecuto "docker compose up -d"
  Entonces PostgreSQL acepta conexiones con los esquemas bronze, silver y gold creados
  Y Metabase responde en el puerto configurado
```

**HU-02** · Andrey · Sprint 4 · Prioridad Alta · RNF-01, RF-08
Como evaluador, quiero instalar y ejecutar el proyecto en mi máquina siguiendo solo el README, para verificar su funcionamiento sin ayuda del equipo.

```gherkin
Escenario: Instalación en una máquina limpia
  Dado una máquina con Docker y Python instalados y sin datos previos del proyecto
  Cuando sigo los pasos del README en orden
  Entonces el pipeline termina sin errores
  Y puedo abrir el tablero con datos cargados
```

### Épica 2 — Ingesta de datos

**HU-03** · David · Sprint 2 · Prioridad Alta · RF-01, RF-02
Como analista financiero, quiero que la TRM histórica desde 2020 se cargue automáticamente desde datos.gov.co, para no descargarla a mano.

```gherkin
Escenario: Carga completa de la TRM
  Dado que la API Socrata de datos.gov.co está disponible
  Cuando ejecuto el extractor de TRM
  Entonces la tabla bronze de TRM contiene registros desde el 1 de enero de 2020
  Y cada registro tiene la fuente, la fecha y hora de carga y el identificador del lote
```

**HU-04** · David · Sprint 2 · Prioridad Alta · RF-01, RF-02
Como analista financiero, quiero que el IPC mensual desde 2020 se cargue desde el Banco de la República, para analizar la inflación junto con la TRM.

```gherkin
Escenario: Carga del IPC
  Dado que el formato de descarga del Banco de la República fue confirmado
  Cuando ejecuto el extractor de IPC
  Entonces la tabla bronze de IPC contiene un registro por mes desde enero de 2020
  Y cada registro conserva el valor original sin transformar y sus metadatos de carga
```

**HU-05** · David · Sprint 2 · Prioridad Alta · RF-01, RF-02
Como analista financiero, quiero que las decisiones de tasa de intervención desde 2020 se carguen desde el Banco de la República, para relacionarlas con la inflación y la TRM.

```gherkin
Escenario: Carga de la tasa de intervención
  Dado que el formato de descarga del Banco de la República fue confirmado
  Cuando ejecuto el extractor de tasa de intervención
  Entonces la tabla bronze contiene cada cambio de tasa con su fecha de vigencia desde 2020
  Y cada registro tiene metadatos de origen y fecha de carga
```

**HU-06** · David · Sprint 2 · Prioridad Media · RF-01
Como integrante del equipo, quiero que los extractores reintenten ante fallas de red y registren los errores, para que una caída temporal de la fuente no rompa el pipeline sin aviso.

```gherkin
Escenario: Falla temporal de la fuente
  Dado que la fuente responde con error en el primer intento
  Cuando el extractor se ejecuta
  Entonces reintenta al menos 3 veces con espera creciente
  Y si todos los intentos fallan, registra el error en el log y termina con código distinto de 0
```

### Épica 3 — Transformación silver

**HU-07** · Juan Esteban · Sprint 3 · Prioridad Alta · RF-03, RF-05
Como analista financiero, quiero la TRM limpia, tipada y sin duplicados, para confiar en los valores diarios.

```gherkin
Escenario: TRM sin duplicados
  Dado que bronze contiene la TRM cargada en dos lotes con fechas repetidas
  Cuando ejecuto "dbt build" sobre silver
  Entonces silver tiene un único registro por fecha
  Y los tests unique y not_null sobre la fecha pasan
```

**HU-08** · Juan Esteban · Sprint 3 · Prioridad Alta · RF-03, RF-01b, RF-05
Como analista financiero, quiero el IPC por mes y la tasa de intervención por periodo de vigencia, para conocer qué tasa regía en cualquier fecha.

```gherkin
Escenario: Tasa de intervención por vigencia
  Dado que bronze contiene los cambios de tasa con su fecha de decisión
  Cuando ejecuto "dbt build" sobre silver
  Entonces cada registro tiene fecha_inicio y fecha_fin de vigencia
  Y los periodos de vigencia no se solapan
```

### Épica 4 — Modelado gold

**HU-09** · Juan Esteban · Sprint 3 · Prioridad Alta · RF-04, RF-01b
Como analista financiero, quiero un modelo estrella con hechos separados por periodicidad y un mart mensual, para comparar TRM, inflación y tasa en el mismo tablero (Opción B).

```gherkin
Escenario: Mart mensual consolidado
  Dado que silver contiene TRM diaria, IPC mensual y tasa por vigencia
  Cuando ejecuto "dbt build" sobre gold
  Entonces existe una dimensión de fecha, un hecho diario de TRM y un hecho mensual de indicadores
  Y el mart mensual tiene una fila por mes con TRM promedio, IPC y tasa vigente
```

**HU-10** · Juan Esteban · Sprint 3 · Prioridad Alta · RF-05
Como integrante del equipo, quiero pruebas de integridad referencial entre hechos y dimensiones, para detectar datos huérfanos antes de que lleguen al tablero.

```gherkin
Escenario: Integridad referencial
  Dado que gold está construido
  Cuando ejecuto "dbt test"
  Entonces el test relationships entre cada hecho y la dimensión de fecha pasa
```

**HU-11** · Juan Esteban · Sprint 3 · Prioridad Media · RF-06, RNF-05
Como analista financiero, quiero consultar de qué fuente y transformación sale cada campo del tablero, para justificar los números que reporto.

```gherkin
Escenario: Consultar el linaje
  Dado que ejecuté "dbt docs generate" y "dbt docs serve"
  Cuando abro el modelo del mart mensual en la documentación
  Entonces el grafo de linaje muestra el camino desde las tablas bronze hasta el mart
  Y cada columna del mart tiene una descripción que indica su origen
```

### Épica 5 — Orquestación

**HU-12** · Andrey · Sprint 3 · Prioridad Alta · RF-08, RNF-02
Como evaluador, quiero ejecutar todo el pipeline con un solo comando, para reproducir los resultados sin conocer los detalles internos.

```gherkin
Escenario: Ejecución de punta a punta
  Dado que el entorno Docker está levantado
  Cuando ejecuto "python pipeline.py"
  Entonces se ejecutan en orden la ingesta de las 2 fuentes y "dbt build"
  Y el script informa la duración total y termina con código 0 si todo fue exitoso
```

### Épica 6 — Visualización

**HU-13** · Andrey · Sprint 4 · Prioridad Alta · RF-07
Como analista financiero, quiero un tablero con la evolución de la TRM, la inflación y la tasa de intervención, para analizar el comportamiento macroeconómico desde 2020.

```gherkin
Escenario: Tablero macroeconómico
  Dado que gold contiene datos desde 2020
  Cuando abro el tablero en Metabase
  Entonces veo al menos 3 visualizaciones: evolución de la TRM, inflación anual y tasa de intervención frente a inflación
  Y puedo filtrar por rango de fechas
```

### Épica 7 — Documentación y trazabilidad (tareas, no HU)

| ID | Tarea | Responsable | Sprint |
|---|---|---|---|
| T-01 | Documento de requisitos RF/RNF | Todos | 1 |
| T-02 | Casos de uso y diagramas de flujo | David | 2 |
| T-03 | Diagrama de arquitectura/componentes | Andrey | 2 |
| T-04 | Modelo de datos (ER de las 3 capas) + ADR Opción B | Juan Esteban | 2 |
| T-05 | Matriz de trazabilidad v1 | Andrey | 2 |
| T-06 | Plan de pruebas y casos de prueba | Juan Esteban | 3 |
| T-07 | Ejecución de pruebas y evidencia | Todos (Juan coordina) | 4 |
| T-08 | Manual técnico y manual de usuario | Andrey | 4 |
| T-09 | Trazabilidad final, actas, retrospectiva general | Andrey (actas), todos (retro) | 4 |

---

## 9. Casos de uso

| ID | Caso de uso | Actor principal | Requisitos |
|---|---|---|---|
| CU-01 | Ejecutar pipeline completo | Evaluador / integrante | RF-08, RNF-02 |
| CU-02 | Ingerir una fuente de datos | Orquestador (sistema) | RF-01, RF-02 |
| CU-03 | Verificar calidad de los datos | Integrante del equipo | RF-05 |
| CU-04 | Consultar el tablero macroeconómico | Analista financiero | RF-07 |
| CU-05 | Consultar el linaje de un campo | Analista financiero | RF-06 |

El detalle de cada caso se escribe con la plantilla 15.2; abajo, CU-01 como ejemplo.

---

## 10. Plan de pruebas (estructura)

### 10.1 Niveles de prueba

| Nivel | Qué se prueba | Herramienta | Responsable | Sprint |
|---|---|---|---|---|
| Unitarias | Extractores: paginación, parseo, reintentos (con respuestas simuladas, sin red) | pytest | David | 2 |
| Calidad de datos | Unicidad, no nulidad, integridad referencial, rangos válidos | Tests dbt | Juan Esteban | 3 |
| Integración | Pipeline completo: fuentes → bronze → silver → gold | `python pipeline.py` + consultas de verificación | Andrey | 3 – 4 |
| Aceptación | Cada HU contra sus escenarios Gherkin | Manual, con evidencia | Quien acepta la HU (sección 5.2) | 2 – 4 |
| Instalación | Proyecto en una máquina limpia | README | Andrey (ejecuta otro integrante) | 4 |
| Rendimiento | Duración del pipeline (fija el umbral de RNF-02) | Medición en `pipeline.py` | Andrey | 3 |

### 10.2 Casos de prueba iniciales

| ID | Descripción | HU | Tipo |
|---|---|---|---|
| CP-ING-01 | El extractor TRM recorre todas las páginas de Socrata | HU-03 | Unitaria |
| CP-ING-02 | El extractor reintenta 3 veces y falla con código distinto de 0 | HU-06 | Unitaria |
| CP-ING-03 | Cada registro bronze tiene metadatos de origen y carga | HU-03, 04, 05 | Integración |
| CP-SIL-01 | TRM en silver única por fecha | HU-07 | Calidad dbt |
| CP-SIL-02 | Vigencias de tasa sin solapamiento | HU-08 | Calidad dbt |
| CP-GLD-01 | Integridad referencial hechos → dim_fecha | HU-10 | Calidad dbt |
| CP-GLD-02 | Mart mensual con una fila por mes desde 2020 | HU-09 | Calidad dbt |
| CP-E2E-01 | Pipeline completo termina con código 0 | HU-12 | Integración |
| CP-DASH-01 | Tablero muestra 3 visualizaciones con datos | HU-13 | Aceptación |
| CP-INST-01 | Instalación en máquina limpia siguiendo el README | HU-02 | Instalación |

### 10.3 Evidencia

Cada ejecución se registra en `docs/pruebas/evidencia/` con fecha, quién la ejecutó, resultado (pasa / falla) y captura o log. Sin CI, esta evidencia es lo único que demuestra que las pruebas se corrieron.

---

## 11. Matriz de trazabilidad base

> Se completa a medida que avanzan los sprints: la columna "Código" se llena con el número de PR y "Estado" con el resultado de la prueba.

| Requisito | Descripción breve | HU | Caso de uso | Código (PR) | Prueba | Estado |
|---|---|---|---|---|---|---|
| RF-01 | Extraer TRM, IPC y tasa | HU-03, 04, 05, 06 | CU-02 | | CP-ING-01, 02 | Pendiente |
| RF-01b | Conciliar periodicidades (Opción B) | HU-08, 09 | — | | CP-SIL-02, CP-GLD-02 | Pendiente |
| RF-02 | Conservar crudos con metadatos | HU-03, 04, 05 | CU-02 | | CP-ING-03 | Pendiente |
| RF-03 | Limpiar, tipar y deduplicar | HU-07, 08 | — | | CP-SIL-01 | Pendiente |
| RF-04 | Esquema estrella en gold | HU-09 | — | | CP-GLD-02 | Pendiente |
| RF-05 | Pruebas automáticas de calidad | HU-07, 08, 10 | CU-03 | | CP-SIL-01, CP-GLD-01 | Pendiente |
| RF-06 | Consultar linaje | HU-11 | CU-05 | | Aceptación HU-11 | Pendiente |
| RF-07 | Tablero con 3+ visualizaciones | HU-13 | CU-04 | | CP-DASH-01 | Pendiente |
| RF-08 | Ejecución con un solo comando | HU-12, 02 | CU-01 | | CP-E2E-01 | Pendiente |
| RNF-01 | Entorno con Docker Compose | HU-01, 02 | CU-01 | | CP-INST-01 | Pendiente |
| RNF-02 | Pipeline en menos de X minutos | HU-12 | CU-01 | | Medición de rendimiento | Pendiente (umbral por definir) |
| RNF-03 | Estándar de estilo | Todas | — | | `verificar.py` | Pendiente |
| RNF-04 | Transformaciones versionadas | Todas | — | Historial Git | — | Pendiente |
| RNF-05 | Documentación dbt automática | HU-11 | CU-05 | | Aceptación HU-11 | Pendiente |

---

## 12. Checklist semanal por integrante

> Cada integrante tiene ~5 h/semana. Marcar al cerrar la semana y reportar lo no completado en la daily asíncrona.

### Semana 2 (28 sep – 4 oct) — cierre del sprint 1

**Todos**
- [ ] Leer este documento y el documento base; anotar desacuerdos.
- [ ] Revisar y numerar los requisitos RF/RNF (T-01).
- [ ] Revisar las HU de la sección 8; David las prioriza como PO.

**David**
- [ ] Probar la API Socrata de TRM: identificar el dataset, paginación y filtro por fecha desde 2020.
- [ ] Confirmar el formato de descarga del IPC y de la tasa de intervención en el Banco de la República (URL, formato, frecuencia).
- [ ] Registrar los hallazgos en `docs/fuentes.md`.

**Juan Esteban**
- [ ] Instalar dbt Core con el adaptador de PostgreSQL y completar el tutorial básico.
- [ ] Redactar el ADR de la Opción B (plantilla 15.7).

**Andrey**
- [ ] Crear el repositorio con la estructura 6.1, proteger `main` y configurar GitHub Projects (6.4).
- [ ] Cargar épicas e HU como issues.
- [ ] Redactar el acta del sprint 1 (plantilla 15.3).

### Semana 3 (5 – 11 oct)

**David**
- [ ] HU-03: extractor de TRM hacia bronze, con pruebas CP-ING-01.
- [ ] Iniciar HU-04: extractor de IPC.
- [ ] T-02: casos de uso CU-01 a CU-05.

**Juan Esteban**
- [ ] T-04: ER de bronze/silver/gold.
- [ ] Inicializar el proyecto dbt y declarar las fuentes (`sources`) apuntando a bronze.

**Andrey**
- [ ] HU-01: Docker Compose con PostgreSQL (esquemas creados) y Metabase. **Prioridad de la semana: bloquea a los demás.**
- [ ] T-03: diagrama de arquitectura/componentes.
- [ ] Crear `verificar.py` (sección 7.1).

### Semana 4 (12 – 18 oct) — ENTREGA DE MITAD

**David**
- [ ] HU-04 y HU-05: extractores del Banco de la República.
- [ ] HU-06: reintentos y registro de errores, con CP-ING-02.
- [ ] T-02: diagramas de flujo de la ingesta.

**Juan Esteban**
- [ ] Revisar y aceptar las HU de ingesta (regla 5.2).
- [ ] Opcional para ganar margen: primer modelo staging de TRM en silver.

**Andrey**
- [ ] T-05: matriz de trazabilidad v1 (sección 11 con PR reales).
- [ ] Actas de los sprints 1 y 2.
- [ ] Ensamblar el documento de la entrega de mitad.

**Todos**
- [ ] Review + retrospectiva del sprint 2 y planning del sprint 3.

### Semana 5 (19 – 25 oct)

- [ ] **Juan Esteban:** HU-07 (TRM en silver) y HU-08 (IPC y tasa por vigencia) con tests.
- [ ] **Juan Esteban:** T-06 plan de pruebas y casos de prueba.
- [ ] **David:** ajustes de ingesta según lo que necesite silver; aceptar las HU de silver.
- [ ] **Andrey:** primera versión de `pipeline.py` (solo ingesta); medir duración.

### Semana 6 (26 oct – 1 nov)

- [ ] **Juan Esteban:** HU-09 (gold, Opción B) y HU-10 (integridad referencial).
- [ ] **Juan Esteban:** HU-11 (descripciones de columnas y `dbt docs`).
- [ ] **Andrey:** HU-12 `pipeline.py` completo (ingesta → `dbt build`); definir el umbral de RNF-02.
- [ ] **David:** actualizar diagramas si el diseño cambió.
- [ ] **Todos:** review + retro del sprint 3 y planning del sprint 4.

### Semana 7 (2 – 8 nov)

- [ ] **Andrey:** HU-13 tablero en Metabase conectado a gold.
- [ ] **Andrey:** T-08 manual técnico y manual de usuario.
- [ ] **Juan Esteban:** coordinar T-07; ejecutar las pruebas de calidad y documentar la evidencia.
- [ ] **David:** ejecutar las pruebas de ingesta e integración; aceptar HU-12 y HU-13 como PO.

### Semana 8 (9 – 15 nov) — ENTREGA FINAL

- [ ] **Andrey:** HU-02 prueba de instalación en máquina limpia (ejecutada por otro integrante).
- [ ] **Andrey:** trazabilidad final y actas de los sprints 3 y 4.
- [ ] **Todos:** retrospectiva general y sección "trabajo futuro".
- [ ] **Todos:** ensamblar el documento final y ensayar la demo (cada uno su parte, ver D-06).

---

## 13. Ceremonias Scrum con fechas

| Ceremonia | Fecha | Duración | Responsable del acta |
|---|---|---|---|
| Review + retro sprint 1 / planning sprint 2 | 4 – 5 oct | 45 min | Andrey |
| Review + retro sprint 2 / planning sprint 3 | 18 – 19 oct | 45 min | Andrey |
| Review + retro sprint 3 / planning sprint 4 | 1 – 2 nov | 45 min | Andrey |
| Review final + retrospectiva general | 14 – 15 nov | 60 min | Andrey |
| Daily asíncrona | Lunes, miércoles y viernes | Mensaje corto | Cada integrante (plantilla 15.6) |

---

## 14. Riesgos actualizados

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| **Inicio tardío:** sprint 1 cierra sin entregables | Ocurrido | Alto | Plan de recuperación (sección 3); registrarlo en el acta del sprint 1 |
| Formato del Banco de la República difícil de automatizar | Media | Medio | Confirmarlo esta semana; contingencia de la sección 3 |
| **PO es también developer** (conflicto de interés al aceptar HU) | Alta | Medio | Regla de aprobación 5.2 |
| **El tablero de Metabase no se reproduce en la máquina del evaluador** (Metabase guarda la configuración del tablero en su base interna, no en el repositorio) | Alta | Alto | Decidir en el sprint 3 cómo se respalda: persistir la base interna de Metabase en un volumen versionado o documentar paso a paso la creación del tablero en el manual. Validar con CP-INST-01 |
| Sin CI, alguien fusiona código que rompe el pipeline | Media | Medio | `verificar.py` obligatorio con evidencia en el PR; `main` protegida |
| Curva de aprendizaje de dbt | Media | Medio | Juan inicia el tutorial en la semana 2 |
| Las 5 h/semana no alcanzan | Alta si se agrega alcance | Alto | Alcance congelado; extras a "trabajo futuro" |
| Desbalance de carga | Baja | Medio | Roles fijos y checklist semanal visible |

---

## 15. Plantillas de artefactos

### 15.1 Historia de usuario (issue de GitHub)

```markdown
**ID:** HU-xx
**Épica:** 
**Requisito(s):** RF-xx / RNF-xx
**Responsable:** 
**Sprint:** 
**Prioridad:** Alta / Media / Baja
**Estimación:** x horas

**Historia**
Como [rol], quiero [acción], para [beneficio].

**Criterios de aceptación**
```gherkin
Escenario: [nombre]
  Dado [contexto]
  Cuando [acción]
  Entonces [resultado esperado]
```

**Aceptada por:** (no puede ser el responsable)
```

### 15.2 Caso de uso

```markdown
## CU-xx: [Nombre]

| Campo | Valor |
|---|---|
| Actor principal | |
| Requisitos | |
| Precondiciones | |
| Postcondiciones | |

**Flujo principal**
1. 
2. 

**Flujos alternativos / excepciones**
- 2a. 
```

**Ejemplo — CU-01: Ejecutar pipeline completo**

| Campo | Valor |
|---|---|
| Actor principal | Evaluador o integrante del equipo |
| Requisitos | RF-08, RNF-01, RNF-02 |
| Precondiciones | Docker y Python instalados; repositorio clonado; `.env` configurado |
| Postcondiciones | Bronze, silver y gold actualizados; tests dbt ejecutados; tablero con datos actuales |

**Flujo principal**
1. El actor ejecuta `docker compose up -d`.
2. El sistema levanta PostgreSQL y Metabase.
3. El actor ejecuta `python pipeline.py`.
4. El sistema ejecuta la ingesta de TRM, IPC y tasa de intervención hacia bronze.
5. El sistema ejecuta `dbt build` (modelos silver y gold con sus tests).
6. El sistema muestra la duración total y termina con código 0.

**Flujos alternativos**
- 4a. Una fuente no responde tras 3 reintentos: el sistema registra el error y termina con código distinto de 0 sin ejecutar dbt.
- 5a. Un test dbt falla: el sistema muestra el test fallido y termina con código distinto de 0.

### 15.3 Acta de sprint

```markdown
# Acta — Sprint N
**Fecha:**  **Asistentes:**  **Duración:**

## Objetivos
- Objetivo del sprint:
- HU comprometidas:

## Completado
| HU | Responsable | Aceptada por | Evidencia (PR) |
|---|---|---|---|

## Pendiente
| HU / tarea | Motivo | Pasa al sprint |
|---|---|---|

## Impedimentos
- 

## Decisiones
- 
```

### 15.4 Caso de prueba

```markdown
| Campo | Valor |
|---|---|
| ID | CP-xxx-nn |
| HU / requisito | |
| Tipo | Unitaria / Calidad dbt / Integración / Aceptación / Instalación |
| Precondiciones | |
| Pasos | 1. … 2. … |
| Datos de prueba | |
| Resultado esperado | |
| Resultado obtenido | |
| Estado | Pasa / Falla |
| Ejecutado por / fecha | |
| Evidencia | ruta a captura o log |
```

### 15.5 Pull Request (`.github/pull_request_template.md`)

```markdown
## Qué hace este PR
Closes #

## HU / requisito
HU-xx — RF-xx

## Verificación local
- [ ] Ejecuté `python verificar.py` sin errores (pegar salida abajo)
- [ ] Agregué o actualicé pruebas
- [ ] Actualicé la documentación

<details><summary>Salida de verificar.py</summary>

```
(pegar aquí)
```
</details>
```

### 15.6 Daily asíncrona

```markdown
**[Nombre] — [fecha]**
- Hice: 
- Haré: 
- Bloqueos: 
```

### 15.7 Registro de decisión de arquitectura (ADR)

```markdown
# ADR-nn: [Título]
**Fecha:**  **Estado:** Propuesta / Aceptada / Reemplazada
**Autor:**  **Aprobada por:**

## Contexto
[Qué problema hay que resolver]

## Opciones consideradas
1. 
2. 

## Decisión
[Qué se eligió]

## Justificación
[Por qué]

## Consecuencias
[Qué implica, ventajas y costos]
```

ADR-01 a redactar esta semana: **Periodicidad mixta — Opción B** (hechos separados por periodicidad, tasa de intervención por vigencia y mart mensual en gold). Es lo que pide el documento base para la sustentación: justificar por escrito la elección.

---

## 16. Próximos pasos (próximas 72 horas)

1. **Andrey:** crear el repositorio, proteger `main` y configurar GitHub Projects con épicas e HU.
2. **David:** probar Socrata y confirmar el formato del Banco de la República; documentar en `docs/fuentes.md`.
3. **Juan Esteban:** instalar dbt y redactar ADR-01.
4. **Todos:** reunión de cierre del sprint 1 (4 o 5 oct): revisar requisitos e HU, aceptar este plan y registrar en el acta el retraso y la decisión de recuperación.
5. **David:** actualizar las secciones 5, 6 y 11 del documento base con los cambios de la sección 1.2.
