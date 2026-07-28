import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()


def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )


def ensure_station_exists(conn, station_id, station_name):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO RAW.STATIONS (station_id, station_name)
        VALUES (%s, %s)
        ON CONFLICT (station_id) DO NOTHING
    """, (station_id, station_name))
    cursor.close()


def load_to_snowflake(df):
    conn = get_snowflake_connection()

    # Bulk load DataFrame into Snowflake
    success, nchunks, nrows, _ = write_pandas(
        conn,
        df,
        table_name="RAW_DISCHARGE",
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema="RAW"
    )

    conn.close()
    return nrows
