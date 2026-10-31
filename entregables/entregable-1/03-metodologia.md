# 3. Justificación de la metodología

**Metodología seleccionada:** Scrum, con prácticas puntuales tomadas de XP.
**Versión:** 1.1 — 25 de octubre de 2026

---

## 1. Características del proyecto que condicionan la elección

| Característica | Dato | Implicación para la metodología |
|---|---|---|
| Equipo | 3 personas | Se descartan marcos de coordinación pesados |
| Duración | 8 semanas desde el 21 de septiembre; quedan 3,7 semanas (26 oct – 20 nov), con una revisión intermedia y la entrega final | Se necesitan incrementos cortos y verificables |
| Dedicación | ~5 h/semana por integrante | El proceso debe tener poca ceremonia |
| Requisitos | Casi todos definidos, con una incertidumbre real: el formato de descarga del Banco de la República | Se necesita absorber cambios sin rehacer el plan |
| Experiencia | Curva de aprendizaje en dbt | Se necesita retroalimentación temprana |
| Evaluación | Se evalúan la gestión, los artefactos y el producto ejecutable | Se necesita equilibrio entre documentación y entrega funcional |
| Riesgo materializado | El sprint 1 cerró sin entregables | El plan debe permitir replanificar sin perder trazabilidad |

## 2. Comparativa de modelos

| Criterio | Cascada | Espiral | Scrum | XP | AUP (Agile Unified Process) |
|---|---|---|---|---|---|
| Tipo | Tradicional, secuencial | Tradicional, iterativo guiado por riesgo | Ágil, marco de gestión | Ágil, prácticas de ingeniería | Ágil, versión simplificada de RUP |
| Manejo del cambio | Muy bajo. El cambio es costoso | Medio. Se revisa cada vuelta | Alto. Se replanifica cada sprint | Muy alto | Medio-alto |
| Entregas funcionales | Al final | Al final de cada ciclo, con prototipos | Incremento al final de cada sprint | Releases muy frecuentes | Incrementos por iteración |
| Gestión del riesgo | Implícita, tardía | Explícita, es su eje central | Mediante backlog, review y retro | Mediante pruebas y feedback continuo | Mediante iteraciones y línea base de arquitectura |
| Documentación | Alta y previa | Alta | Ligera (la necesaria) | Mínima | Media (modelos de UML y casos de uso) |
| Tamaño de equipo ideal | Cualquiera | Equipos medianos y grandes | 3 a 9 personas | 2 a 12 personas, con el cliente presente | Equipos pequeños y medianos |
| Roles definidos | Gerente, analistas, etc. | Variados | PO, Scrum Master, Developers | Cliente, programadores | Variados, tomados de RUP |
| Ajuste a 3 personas y 8 semanas | Bajo | Bajo (mucha sobrecarga de ciclos de riesgo) | **Alto** | Medio (exige disciplina y cliente presente) | Medio (más ceremonia de la necesaria) |

## 3. Decisión y justificación

Se elige **Scrum**, con 4 sprints (el 1 ya cerrado y los sprints 2 a 4 de una semana, más una semana de cierre), por estas razones:

1. **Encaja con la escala.** Tres personas y 8 semanas caben en Scrum sin sobrecarga. La cascada obligaría a congelar los requisitos antes de construir, y la espiral añade ciclos de análisis de riesgo que el equipo no tiene tiempo de ejecutar.
2. **Las entregas coinciden con los sprints.** La revisión intermedia (30 oct, Entregable 2: diseño UML) cae al cierre del sprint 2 y la entrega final (20 nov) tras el sprint 4 y el colchón. Cada sprint tiene un objetivo verificable (ver `02-planeacion-cronograma.md`).
3. **Absorbe la incertidumbre.** El formato del Banco de la República no está confirmado. En Scrum, ese riesgo se gestiona con el backlog y una contingencia (TRM completa y extractor parcial) sin romper el plan.
4. **Permitió recuperarse del retraso.** Cuando el sprint 1 cerró sin entregables, el equipo movió el trabajo al sprint 2 y registró el retraso como impedimento en el acta. Con cascada, ese mismo retraso habría desplazado todas las fases siguientes.
5. **Da evidencia de gestión.** Las actas, el backlog, la revisión y la retrospectiva producen artefactos evaluables.
6. **Reparte la responsabilidad.** El rol de cada persona (PO, Scrum Master, developers) es explícito, y cada integrante sustenta su parte (D-06).

### 3.1 Por qué no los otros

| Modelo | Motivo de descarte |
|---|---|
| Cascada | Exige requisitos y diseño cerrados desde el inicio y no deja espacio al aprendizaje de dbt ni a la incertidumbre de la fuente |
| Espiral | Su fortaleza es el análisis formal de riesgos en proyectos grandes. Aquí el costo del proceso supera el beneficio |
| XP | Sus prácticas son valiosas, pero depende de un cliente presente de forma continua y de disciplina que 5 h/semana no sostienen completa. Se adoptan prácticas sueltas (ver más abajo) |
| AUP | Pide más modelado y fases formales (inicio, elaboración, construcción, transición) de lo que el proyecto necesita. Se toma de él la idea de documentar el diseño (casos de uso, arquitectura) en paralelo al código |

## 4. Cómo se aplica Scrum en este proyecto

| Elemento de Scrum | Aplicación |
|---|---|
| Roles | David: Product Owner + desarrollador de ingesta · Andrey: Scrum Master + desarrollador · Juan Esteban: desarrollador |
| Sprints | Sprint 1 (21 sep – 25 oct, cerrado sin entregables técnicos), tres sprints de una semana (26 oct – 15 nov) y una semana de cierre (16 – 20 nov) |
| Product Backlog | 14 historias de usuario en 7 épicas (`06-product-backlog.md`) |
| Sprint Backlog | Historias asignadas por sprint con responsable y estimación |
| Daily | Asíncrona (lunes, miércoles y viernes), un mensaje corto por integrante |
| Review y retrospectiva | Al cierre de cada sprint (45 min) y una final (60 min) |
| Definition of Ready | HU con formato "Como… quiero… para…", escenario Gherkin, requisito enlazado, responsable y estimación |
| Definition of Done | PR aprobado por otro integrante, `verificar.py` sin errores, prueba asociada, documentación actualizada y criterios de aceptación verificados |
| Incremento | Bronze funcionando (sprint 2), silver y gold (sprint 3) y tablero instalable (sprint 4) |

### 4.1 Adaptaciones al contexto

| Adaptación | Motivo |
|---|---|
| **Regla de aprobación.** El PO no acepta sus propias historias | David es PO y desarrollador a la vez. Sus HU las acepta Juan o Andrey |
| **Daily asíncrona** en lugar de reunión diaria | Los integrantes dedican ~5 h/semana y no coinciden a diario |
| **Verificación local obligatoria** (`verificar.py`) en lugar de CI | Decisión D-07: no hay integración continua |
| **Diseño en paralelo al código** | Plan de recuperación: la documentación de diseño no puede esperar al final |

### 4.2 Prácticas de XP incorporadas

| Práctica | Cómo aparece en el proyecto |
|---|---|
| Pruebas automatizadas | `pytest` para extractores y tests de dbt para calidad de datos |
| Revisión por pares | Todo PR requiere la aprobación de otra persona |
| Integración frecuente | Ramas cortas desde `main` y squash merge |
| Estándar de código | `ruff` (PEP 8) y, opcionalmente, `sqlfluff` |
| Entregas pequeñas | Incrementos por sprint con objetivo verificable |

## 5. Limitaciones asumidas

- Con 5 h/semana por persona, los sprints entregan menos de lo que Scrum asume en equipos de dedicación completa.
- El Product Owner es parte del equipo de desarrollo, lo que reduce la separación de roles. La regla de aprobación lo mitiga, pero no lo elimina.
- No hay un cliente real disponible de forma continua. El profesor actúa como evaluador y el rol de "analista financiero" se representa mediante la elicitación (ver `04-elicitacion.md`).
