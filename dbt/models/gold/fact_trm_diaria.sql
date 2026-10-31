-- Hecho diario de la TRM: una fila por día calendario, tomada de silver.
select
    fecha,
    valor,
    vigencia_desde,
    vigencia_hasta,
    lote_id
from {{ ref('silver_trm') }}
