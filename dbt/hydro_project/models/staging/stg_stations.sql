{{ config(materialized='view') }}

select
    STATION_ID,
    STATION_NAME
from {{ source('raw', 'STATIONS') }}
