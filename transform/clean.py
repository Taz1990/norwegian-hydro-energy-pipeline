####### ..........Block 6: Transform or clean extracted data......#######
import json
import pandas as pd
import os


def clean_dataframe(df):

    # Step 1: convert time column to datetime
    df['time'] = pd.to_datetime(df['time'])

    # Step 2: sort by time
    df = df.sort_values('time')

    # Step 3: Drop duplicates (station_id + time = unique key)
    df = df.drop_duplicates(subset=['station_id', 'time'])

    # Step 4: Add load timestamp
    df['load_timestamp'] = pd.Timestamp.now('UTC')

    # Step 5: Reset index
    df = df.reset_index(drop=True)
    return df


def transform(input_data):
    if input_data is None:
        print("Transform skipped: no input data")
        return None

    running_in_airflow = "AIRFLOW_HOME" in os.environ

    if running_in_airflow:
        # input_data is a file path to RAW JSON
        with open(input_data, "r") as f:
            raw = json.load(f)

        observations = raw["data"][0]["observations"]
        df = pd.DataFrame(observations)

        df["station_id"] = raw["data"][0]["stationId"]
        df["station_name"] = raw["data"][0]["stationName"]
        df["unit"] = raw["data"][0]["unit"]

        clean_df = clean_dataframe(df)
        return clean_df.to_json()

    else:
        df = input_data
        clean_df = clean_dataframe(df)
        return clean_df


def run_transform(input_data):
    return transform(input_data)


if __name__ == "__main__":
    from extract.NVEapi import extract

    df, file_name = extract(
        station_id='12.228.0',
        parameter='1001',
        resolution='60',
        days_back=3
    )

    # Local mode: pass DataFrame directly
    clean_data = transform(df)

    print(clean_data.head())
    print(len(clean_data))
    print(clean_data[:3])
