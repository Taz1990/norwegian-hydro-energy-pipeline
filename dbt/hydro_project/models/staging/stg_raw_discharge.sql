{{ config(materialized='view') }}

with source as (
    select
        station_id,
        timestamp,
        value,
        quality,
        unit,
        load_timestamp
    from {{ source('raw', 'RAW_DISCHARGE') }}
    where station_id is not null
      and timestamp is not null
      and value is not null
),

deduped as (
    select
        *,
        row_number() over (
            partition by station_id, timestamp
            order by load_timestamp desc
        ) as rn
    from source
)

select
    station_id,
    timestamp,
    value,
    quality,
    unit,
    load_timestamp
from deduped
where rn = 1
