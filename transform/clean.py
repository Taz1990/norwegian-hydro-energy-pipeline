#######..........Block 6: Transform or clean extracted data......#######
import pandas as pd

def clean_dataframe(df):
    
    # Step 1: convert time column to datetime
    df['time'] = pd.to_datetime(df['time'])
    
    # step 2: sort by time
    df = df.sort_values('time')
    
    # step 3: Drop duplicates
    df = df.drop_duplicates(subset=['station_id', 'time'])
    
    #step 4: Add load Timestamp
    df['load_timestamp'] = pd.Timestamp.now('UTC')
    
    # step 5: Reset index
    df = df.reset_index(drop=True)
    return df

def transform(df):
    
    clean_data = clean_dataframe(df)
    return clean_data

if __name__ == "__main__":
    from extract.NVEapi import extract
    df, file_name = extract(
            station_id= '12.228.0',
            parameter= '1001',
            resolution= '60',
            days_back= 3
        )
    clean_data = transform(df)
    print(clean_data.head)