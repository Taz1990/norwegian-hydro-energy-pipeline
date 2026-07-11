#######..........Block 6: Transform or clean extracted data......#######
import pandas as pd
import os


def clean_dataframe(df):
    # Extract nested observations
    observations = df["data"][0]["observations"]
    obs_df = pd.DataFrame(observations)

    # Convert time column to datetime
    obs_df["time"] = pd.to_datetime(obs_df["time"])

    # Add station metadata (correct JSON structure)
    station_id = df["data"][0]["stationId"]
    station_name = df["data"][0]["stationName"]
    unit = df["data"][0]["unit"]
    load_timestamp = pd.Timestamp.now()

    obs_df["station_id"] = station_id
    obs_df["station_name"] = station_name
    obs_df["unit"] = unit
    obs_df["load_timestamp"] = load_timestamp

    return obs_df



def transform(input_data):
    """
    Dual-mode transform:
    - Airflow: input_data = file_name (string)
    - Local:   input_data = DataFrame OR file_name
    """
    if input_data is None:
        print("Transform skipped: no input data")
        return None

    # If input_data is a file path → read JSON
    if isinstance(input_data, str):
        df = pd.read_json(input_data)
    else:
        # If input_data is a DataFrame → use it directly
        df = input_data

    # Clean the DataFrame
    clean_df = clean_dataframe(df)

    # Airflow needs JSON-safe output for XCom
    if "AIRFLOW_HOME" in os.environ:
        return clean_df.to_json()

    # Local mode returns a DataFrame
    return clean_df


def run_transform(input_data):
    return transform(input_data)

if __name__ == "__main__":
    from extract.NVEapi import extract
    from transform.clean import transform
    df, file_name = extract(
            station_id= '12.228.0',
            parameter= '1001',
            resolution= '60',
            days_back= 3
        )
    print(df.keys())
    print(df["data"][0].keys())   
    clean_data = transform(file_name)
    print(clean_data.head)
    
    print(len(clean_data))
    print(clean_data[:3])
    print(df.keys())
    print(df["data"][0].keys())

'''
As extract is outside transform folder it will show module not found error if we will run this programm directly
To avoid it run "python -m transform.clean" inside terminal as a command.
'''
