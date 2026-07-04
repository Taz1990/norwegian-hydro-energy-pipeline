{{ config(materialized='view') }}

with source as (
    select
        station_id,
        station_name,
        time,
        value,
        quality,
        unit,
        load_timestamp
    from {{ source('postgres', 'raw_discharge') }}
),

deduped as (
    select
        *,
        row_number() over (
            partition by station_id, time
            order by load_timestamp desc
        ) as rn
    from source
)

select
    station_id,
    station_name,
    time,
    value::float,
    quality,
    unit,
    load_timestamp
from deduped
where rn = 1
