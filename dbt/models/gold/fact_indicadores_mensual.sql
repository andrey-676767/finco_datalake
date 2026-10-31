-- Hecho mensual de indicadores: una fila por mes desde enero de 2020.
-- IPC (índice), inflación anual y tasa de intervención vigente el último día del mes.
-- El IPC de 2019 solo se usa para calcular la inflación anual de 2020.
with ipc as (
    select
        mes as anio_mes,
        indice as ipc,
        round((indice / lag(indice, 12) over (order by mes) - 1) * 100, 2) as inflacion_anual
    from {{ ref('silver_ipc') }}
)

select
    ipc.anio_mes,
    ipc.ipc,
    ipc.inflacion_anual,
    tasa.tasa as tasa_vigente
from ipc
left join {{ ref('silver_tasa_intervencion') }} as tasa
    on (ipc.anio_mes + interval '1 month' - interval '1 day')::date
       between tasa.fecha_inicio and tasa.fecha_fin
where ipc.anio_mes >= date '2020-01-01'
