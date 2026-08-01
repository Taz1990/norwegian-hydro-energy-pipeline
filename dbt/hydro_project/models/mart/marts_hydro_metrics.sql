{{ config
(materialized='table') }}

with
    daily
    as
    (
        select *
        from {{ ref
    ('core_daily_summary') }}
),

stations as
(
    select
    STATION_ID,
    STATION_NAME
from {{ source('raw', 'STATIONS') }}
)

select
    d.station_id,
    s.station_name,
    d.date,
    d.min_discharge,
    d.max_discharge,
    d.avg_discharge,
    d.measurements,
    d.avg_discharge 
        - lag(d.avg_discharge) over (
            partition by d.station_id 
            order by d.date
        ) as discharge_trend
from daily d
    left join stations s
    on d.station_id = s.station_id
