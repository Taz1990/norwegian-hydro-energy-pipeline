{{ config
(materialized='table') }}

with
    base
    as
    (
        select
            station_id,
            timestamp::timestamp as ts,
            value::float as discharge
        from {{ ref('stg_raw_discharge') }}
        
),

daily as
(
    select
    station_id,
    date_trunc('day', ts) as date,
    min(discharge) as min_discharge,
    max(discharge) as max_discharge,
    avg(discharge) as avg_discharge,
    count(*) as measurements
from base
group by station_id, date
)

select *
from daily
