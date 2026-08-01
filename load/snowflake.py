import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()


# -----------------------------
# CONNECTION
# -----------------------------
def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )


# -----------------------------
# ENSURE STATION EXISTS (Snowflake-safe)
# -----------------------------
def ensure_station_exists(conn, station_id, station_name):
    cursor = conn.cursor()

    # Snowflake does NOT support ON CONFLICT → use MERGE
    cursor.execute("""
        MERGE INTO RAW.STATIONS AS target
        USING (SELECT %(station_id)s AS station_id, %(station_name)s AS station_name) AS source
        ON target.STATION_ID = source.station_id
        WHEN NOT MATCHED THEN
            INSERT (STATION_ID, STATION_NAME)
            VALUES (source.station_id, source.station_name)
    """, {
        "station_id": station_id,
        "station_name": station_name
    })

    cursor.close()


# -----------------------------
# LOAD SINGLE RECORD (Airflow uses this)
# -----------------------------
def load_record_to_snowflake(record):
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO RAW.RAW_DISCHARGE (
            STATION_ID,
            TIMESTAMP,
            VALUE,
            QUALITY,
            UNIT,
            LOAD_TIMESTAMP
        )
        VALUES (
            %(station_id)s,
            %(timestamp)s,
            %(value)s,
            %(quality)s,
            %(unit)s,
            %(load_timestamp)s
        )
    """, record)

    conn.commit()
    cursor.close()
    conn.close()
    print("RECORD RECEIVED BY LOADER:", record)
