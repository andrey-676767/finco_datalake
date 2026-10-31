{{ config(alias='trm') }}

-- TRM diaria: una fila por día calendario.
-- Bronze publica la TRM por vigencia (desde-hasta); aquí cada vigencia se expande a sus días.
-- Si un día aparece en dos lotes, gana el lote más reciente.
with tipada as (
    select
        id,
        lote_id,
        cargado_en,
        valor::numeric as valor,
        vigenciadesde::timestamp::date as vigencia_desde,
        vigenciahasta::timestamp::date as vigencia_hasta
    from {{ source('bronze', 'trm_raw') }}
),

dias as (
    select
        generate_series(vigencia_desde, vigencia_hasta, interval '1 day')::date as fecha,
        *
    from tipada
),

ordenada as (
    select
        *,
        row_number() over (partition by fecha order by cargado_en desc, id desc) as posicion
    from dias
)

select
    fecha,
    valor,
    vigencia_desde,
    vigencia_hasta,
    lote_id,
    cargado_en
from ordenada
where posicion = 1
