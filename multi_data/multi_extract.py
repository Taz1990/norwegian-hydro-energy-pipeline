'''
Loops through STATIONS
Extracts discharge
Cleans
Loads into RAW
Uses logging
'''
import logging
from extract.NVEapi import extract
from transform.clean import transform
from load.postgresql import load_to_postgresql
from dotenv import load_dotenv
import os 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def multi_station_pipeline(stations, days_back=3):
    total_rows = 0

    for station in stations:
        logging.info(f"Fetching station: {station}")

        result = extract(
            station_id=station,
            parameter="1001",
            resolution="60",
            days_back=3
    )

        if result is None:
            logging.warning(f"No data for station {station}. Skipping.")
            continue

        df, file_name = result

        clean_df = transform(df)
        rows = load_to_postgresql(clean_df)
        
        logging.info(f'Extraction complete. Raw file saved: {file_name}')
        logging.info(f"Inserted {rows} rows for station {station}")
        total_rows += rows

    logging.info(f"Total rows inserted: {total_rows}")
    return total_rows


if __name__ == "__main__":
    
    load_dotenv()

    raw_stations = os.getenv("STATIONS").split(",")
    stations = [item.split(":")[0] for item in raw_stations]

    multi_station_pipeline(stations)
