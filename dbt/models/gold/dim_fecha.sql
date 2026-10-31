-- Dimensión de fecha: un día calendario por fila.
-- Empieza en `fecha_inicio_dim` (2019-01-01: el IPC arranca en enero de 2019) y llega al último día con TRM en silver.
select
    d::date as fecha,
    extract(year from d)::int as anio,
    extract(month from d)::int as mes,
    extract(quarter from d)::int as trimestre,
    date_trunc('month', d)::date as anio_mes,
    extract(isodow from d)::int as dia_semana,
    extract(isodow from d) in (6, 7) as es_fin_de_semana
from generate_series(
    '{{ var("fecha_inicio_dim") }}'::date,
    (select max(fecha) from {{ ref('silver_trm') }}),
    interval '1 day'
) as d
