# Datos financieros públicos (finco_datalake)

Lakehouse analítico que consolida indicadores macroeconómicos colombianos públicos (TRM, IPC y tasa de intervención) en capas, para compararlos en un tablero.

## Language

**Lakehouse**:
Arquitectura moderna del proyecto: bronze vive como archivos Parquet inmutables (el lake) y silver y gold se modelan con dbt en PostgreSQL (el house), organizados en capas.
_Avoid_: Data warehouse, data lake

**Réplica de bronze**:
Copia en PostgreSQL (`bronze.*`) de cada lote Parquet, para que dbt pueda construir silver y gold. El Parquet es la fuente de verdad.
_Avoid_: Tabla bronze original

**Capa (bronze / silver / gold)**:
Cada nivel de refinamiento de los datos: bronze guarda el dato original, silver el dato limpio y tipado, gold el dato modelado para análisis.
_Avoid_: Zona, nivel

**Lote**:
Una ejecución de carga de una fuente, identificada de forma única. Los registros de lotes anteriores nunca se modifican.
_Avoid_: Batch, corrida

**TRM**:
Tasa Representativa del Mercado: tasa de cambio peso-dólar. La fuente la publica por vigencia; en silver se expande a un registro por día calendario.
_Avoid_: Dólar, tasa de cambio

**IPC**:
Índice de Precios al Consumidor: indicador de inflación, publicado con periodicidad mensual.
_Avoid_: Inflación (la inflación es lo que se deriva del IPC)

**Tasa de intervención**:
Tasa de política monetaria fijada por la Junta del Banco de la República; cambia solo cuando la Junta decide.
_Avoid_: Tasa de interés, tasa repo

**Vigencia**:
Periodo (`fecha_inicio` a `fecha_fin`) durante el cual un valor rigió. Aplica a la TRM (fines de semana y festivos repiten el valor del último día hábil) y a la tasa de intervención (las vigencias no se solapan).
_Avoid_: Periodo de validez

**Inflación anual**:
Variación porcentual del IPC de un mes frente al mismo mes del año anterior. Exige cargar el IPC desde enero de 2019.
_Avoid_: IPC (el IPC es el índice, no su variación)

**CSV exportado**:
Archivo descargado a mano del Banco de la República y versionado en el repositorio; es la fuente de bronze para IPC y tasa de intervención.
_Avoid_: Extractor del Banco

**Mart mensual**:
Tabla de gold con una fila por mes que consolida la TRM promedio, el IPC y la tasa de intervención vigente.
_Avoid_: Vista consolidada, cubo

**Evaluador**:
El profesor, que instala y ejecuta el proyecto en su propia máquina siguiendo solo el README.
_Avoid_: Cliente, usuario final

**Tablero**:
Conjunto de visualizaciones del proyecto en Metabase, entregado ya cargado con datos.
_Avoid_: Dashboard, panel

**Aplicación de extracción**:
Aplicación web aparte del tablero donde el analista visualiza los datos de gold y los descarga filtrados.
_Avoid_: Dashboard de extracción, portal

**Revisión intermedia**:
Revisión parcial del proyecto por el profesor el 30 de octubre de 2026; evalúa el Entregable 2 (análisis y diseño UML).
_Avoid_: Entrega de mitad
