{{ config(alias='tasa_intervencion') }}

-- Tasa de política monetaria por periodo de vigencia, sin solapes.
-- Bronze trae un valor por día; los días consecutivos con la misma tasa se colapsan.
-- Si un día aparece en dos lotes, gana el lote más reciente.
-- Solo quedan los periodos que terminan el 2020-01-01 o después.
with tipada as (
    select
        id,
        cargado_en,
        (fila->>'Periodo(MMM DD, AAAA)')::date as fecha,
        trim_scale((fila->>'Tasa de política monetaria')::numeric) as tasa
    from {{ source('bronze', 'tasa_intervencion_raw') }}
),

diaria as (
    select fecha, tasa
    from (
        select
            *,
            row_number() over (partition by fecha order by cargado_en desc, id desc) as posicion
        from tipada
    ) t
    where posicion = 1
),

marcada as (
    select
        *,
        case when tasa is distinct from lag(tasa) over (order by fecha) then 1 else 0 end as cambia
    from diaria
),

grupos as (
    select *, sum(cambia) over (order by fecha) as grupo
    from marcada
),

periodos as (
    select
        min(fecha) as fecha_inicio,
        max(fecha) as fecha_fin,
        tasa
    from grupos
    group by grupo, tasa
)

select fecha_inicio, fecha_fin, tasa
from periodos
where fecha_fin >= date '2020-01-01'
