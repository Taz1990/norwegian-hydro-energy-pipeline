{{ config(materialized='view') }}

select
    station_id,
    timestamp,
    value,
    quality,
    unit,
    load_timestamp
from {{ source('raw', 'RAW_DISCHARGE') }}
