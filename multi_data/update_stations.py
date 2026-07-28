''' 
To stop the Foreign Kye violation error
Calls NVE metadata API
Filters discharge stations
Inserts station_id + station_name
Uses ON CONFLICT DO NOTHING
Runs once before extraction
'''
import requests
import psycopg2
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

# Format in .env:
# STATIONS=12.228.0:Kistefoss, 29.4.0:Aspervik, 15.250.0:Glomma, 15.70.0:Trysilelva
raw_stations = os.getenv("STATIONS").split(",")

STATIONS = {}
for item in raw_stations:
    station_id, station_name = item.split(":")
    STATIONS[station_id] = station_name


def update_stations_table():
    conn = psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )
    cur = conn.cursor()

    for station_id, fallback_name in STATIONS.items():
        url = f"https://api.nve.no/hydrology/v1/discharge/{station_id}"
        logging.info(f"Fetching metadata for station {station_id}")

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()["data"][0]
            station_name = data["stationName"]
        else:
            logging.warning(
                f"No live data for {station_id}, using fallback name.")
            station_name = fallback_name

        cur.execute("""
            INSERT INTO stations (station_id, station_name)
            VALUES (%s, %s)
            ON CONFLICT (station_id) DO NOTHING;
        """, (station_id, station_name))

    conn.commit()
    cur.close()
    conn.close()

    logging.info("Stations table updated successfully.")


if __name__ == "__main__":
    update_stations_table()
