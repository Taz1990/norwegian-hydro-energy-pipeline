
{{ config
(materialized='view') }}

with
    source
    as
    (
        select
            STATION_ID,
            TIMESTAMP ,
            VALUE,
            QUALITY,
            UNIT,
            LOAD_TIMESTAMP
        from {{ source('raw', 'RAW_DISCHARGE') }}
),

deduped as
(
    select
    *,
    row_number() over (
            partition by STATION_ID, TIMESTAMP
            order by LOAD_TIMESTAMP desc
        ) as rn
from source
)

select
    STATION_ID,
    TIMESTAMP as time,
    VALUE::float as value,
    QUALITY,
    UNIT,
    LOAD_TIMESTAMP
from deduped
where rn = 1
