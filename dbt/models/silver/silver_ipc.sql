{{ config(alias='ipc') }}

-- IPC mensual: una fila por mes desde enero de 2019.
-- Bronze guarda la fila completa del CSV como jsonb (texto); aquí se tipa.
-- Si un mes aparece en dos lotes, gana el lote más reciente.
with tipada as (
    select
        id,
        lote_id,
        cargado_en,
        date_trunc('month', to_date(fila->>'Periodo(MMM, AAAA)', 'YYYY/MM/DD'))::date as mes,
        (fila->>'Índice de Precios al Consumidor (IPC)')::numeric as indice
    from {{ source('bronze', 'ipc_raw') }}
),

ordenada as (
    select
        *,
        row_number() over (partition by mes order by cargado_en desc, id desc) as posicion
    from tipada
    where mes >= date '2019-01-01'
)

select mes, indice, lote_id, cargado_en
from ordenada
where posicion = 1
