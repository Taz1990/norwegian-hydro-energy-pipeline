{{ config(materialized='view') }}

select
    station_id,
    station_name,
    river_name,
    county,
    latitude::float as latitude,
    longitude::float as longitude,
    elevation_m::float as elevation_m,
    active,
    created_at,
    updated_at
from {{ source('postgres', 'stations') }}
where latitude is not null
  and longitude is not null
