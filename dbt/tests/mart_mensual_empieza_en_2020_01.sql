-- CP-GLD-02: el mart mensual arranca en 2020-01. Devuelve filas (y falla) si el primer mes es otro.
select min(anio_mes) as primer_mes
from {{ ref('mart_mensual') }}
having min(anio_mes) <> date '2020-01-01'
