##### .............. Block 7: load cleaned data to Postgresql.............#####

import os
import psycopg2
import psycopg2.extras  # that gives advanced PostgreSQL features
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # to load theAPI key and other variables into Docker for postgresql

"""
Create a PostgreSQL connection using environment variables which are inside .env file.
connect_db() reads .env values and uses them to open a PostgreSQL connection using psycopg2.
"""


def connect_db():

    conn = psycopg2.connect(
        host=os.getenv('PG_HOST'),
        database=os.getenv('PG_DATABASE'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASSWORD'),
        port=os.getenv('PG_PORT')
    )
    return conn

# to resolve the foreign key issue


def ensure_station_exists(df):
    conn = connect_db()
    curs = conn.cursor()

    station_id = df['station_id'].iloc[0]
    station_name = df['station_name'].iloc[0]

    curs.execute("""
        INSERT INTO stations (station_id, station_name)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
    """, (station_id, station_name))

    conn.commit()  # saves the changes into PostgreSQL
    curs.close()  # close SQL command tool
    conn.close()  # close database connection


def load_to_postgresql(input_data):
    """
    Load cleaned DataFrame into raw_discharge table.
    This function takes a cleaned DataFrame, converts it to tuples,
    and inserts all rows into the raw_discharge table in PostgreSQL
    """
    """
    Dual-mode load:
    - Airflow: input_data = JSON string
    - Local:   input_data = DataFrame
    """
    running_in_airflow = os.getenv("AIRFLOW__CORE__EXECUTOR") is not None
    if running_in_airflow:
        df = pd.read_json(input_data)
        # FIX: convert UNIX ms → timestamp
        df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
        df["load_timestamp"] = pd.to_datetime(
            df["load_timestamp"], unit="ms", utc=True)
    else:
        df = input_data

    # FIX FOREIGN KEY HERE
    ensure_station_exists(df)

    conn = connect_db()
    # A cursor is the object that sends SQL commands to PostgreSQL.
    curs = conn.cursor()
    # the table raw_discharge has been created before inside docker to postgresql DB using command prompt now insert the values into the table
    insert_query = """
        INSERT INTO raw_discharge(
            station_id,
            station_name,
            time,
            value,
            quality,
            unit,
            load_timestamp
        )
        VALUES %s
        ON CONFLICT (station_id, time) DO NOTHING;
        
    """
    # Keep only the columns that exist in the SQL table
    df = df[["station_id", "station_name", "time",
             "value", "quality", "unit", "load_timestamp"]]

    # Convert df to list of tuples
    records = list(df.itertuples(index=False, name=None))

    psycopg2.extras.execute_values(
        curs,
        insert_query,
        records,
        template=None,
        page_size=1000
    )

    conn.commit()  # saves the changes into PostgreSQL
    curs.close()  # close SQL command tool
    conn.close()  # close database connection

    return len(records)


if __name__ == "__main__":
    from extract.NVEapi import extract
    from transform.clean import transform
    df, file_name = extract(
        station_id='12.228.0',
        parameter='1001',
        resolution='1440',
        days_back=3
    )
    clean_data = transform(df)
    rows = load_to_postgresql(clean_data)
    print(f'Inserted rows: {rows}')
    print(clean_data)
