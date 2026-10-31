-- Mart mensual: una fila por mes con TRM promedio, IPC, inflación anual y tasa vigente.
select
    ind.anio_mes,
    round(avg(trm.valor), 2) as trm_promedio,
    ind.ipc,
    ind.inflacion_anual,
    ind.tasa_vigente
from {{ ref('fact_indicadores_mensual') }} as ind
left join {{ ref('fact_trm_diaria') }} as trm
    on date_trunc('month', trm.fecha)::date = ind.anio_mes
group by ind.anio_mes, ind.ipc, ind.inflacion_anual, ind.tasa_vigente
