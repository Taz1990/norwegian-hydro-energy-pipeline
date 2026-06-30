
-- RAW LAYER: API data (append-only)
-- Used by: pipeline.py, Airflow, dbt staging

CREATE TABLE IF NOT EXISTS raw_discharge (
    station_id      VARCHAR(20)        NOT NULL,
    station_name    VARCHAR(100),
    time            TIMESTAMP          NOT NULL,
    value           DOUBLE PRECISION,
    quality         VARCHAR(20),
    unit            VARCHAR(20),
    load_timestamp  TIMESTAMP          DEFAULT NOW(),

    PRIMARY KEY (station_id, time)
);

-- Index for fast time-based queries (dbt + PySpark + Streamlit)
CREATE INDEX IF NOT EXISTS idx_raw_discharge_time
    ON raw_discharge (time);



-- DIMENSION LAYER: Station metadata 
-- Used by: dbt dim_stations, PySpark joins, dashboards

CREATE TABLE IF NOT EXISTS stations (
    station_id       VARCHAR(20)   PRIMARY KEY,
    station_name     VARCHAR(100)  NOT NULL,
    river_name       VARCHAR(100),
    county           VARCHAR(100),
    latitude         FLOAT,
    longitude        FLOAT,
    elevation_m      FLOAT,
    active           BOOLEAN       DEFAULT TRUE,
    created_at       TIMESTAMP     DEFAULT NOW(),
    updated_at       TIMESTAMP     DEFAULT NOW()
);

-- Enforce data quality: raw_discharge must reference a valid station
ALTER TABLE raw_discharge
    ADD CONSTRAINT fk_raw_station
    FOREIGN KEY (station_id)
    REFERENCES stations (station_id);



-- CURATED LAYER: Daily summary (analytics-ready)
-- Used by: dbt fact models, PySpark aggregations, Streamlit dashboards

CREATE TABLE IF NOT EXISTS discharge_daily_summary (
    station_id      VARCHAR(20)   NOT NULL,
    date            DATE          NOT NULL,
    avg_value       DOUBLE PRECISION,
    min_value       DOUBLE PRECISION,
    max_value       DOUBLE PRECISION,
    readings_count  INTEGER,
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (station_id, date)
);

-- Index for fast dashboard filtering
CREATE INDEX IF NOT EXISTS idx_daily_summary_date
    ON discharge_daily_summary (date);
