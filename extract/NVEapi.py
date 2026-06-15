                    #####....Block-1: import+load....######
"""To extract data from web API, download raw data, load api key"""

import requests
import  os
from dotenv import load_dotenv

#for block-3
from datetime import datetime
import json
import logging
###############################

load_dotenv() #to load the API key

API_read = os.getenv("NVE-API-KEY") #get API
#print(API_read)

#Base api url for observation dataset contains measured values
base_api_url = "https://hydapi.nve.no/api/v1/Observations"

##run this if condition after Block 1 & comment it after Block 2 if condition...........
#now check api & url
''' 
if __name__ == "__main__":
    if API_read:
        print(f"The API Key is: {API_read[:6]}")
        print(f"The base url is: {base_api_url}")
    else:
        print("Error! NO API found in .env")
'''



                #####....Block-2: Data fetch from API ....#####
# To get hourly water flow readings from the Kistefoss station on the Randselva river for the last 3 days'''               
 
"""
    Fetch observations for one NVE station.

    station_id  : the station code  e.g. "12.228.0"
    parameter   : the data type     e.g. "1001" = discharge
    resolution  : time interval     e.g. "60"   = hourly
    days_back   : how many days     e.g. 3      = last 3 days
"""               
def fetch_station(station_id, parameter,resolution,days_back=3):              
                
    headers= { 'X-API-KEY': API_read,
               'accept': 'application/json'
            }  
    params= {
        "StationId": station_id,
        "Parameter": parameter,
        "ResolutionTime": resolution,
        "ReferenceTime": f'P{days_back}D/'
            }              
                
    print(f"Calling NVE API...")
    print(f"Station : {station_id}")
    print(f"Parameter: {parameter}")
    print(f"Last {days_back} days")            
     
    #HTTPS request package            
    response= requests.get (
        base_api_url,
        headers=headers,
        params=params,
        timeout=30
    )     
    
    print(f"status code: {response.status_code}") 
    
    data= response.json()
    return data    

###............. Block-3: Save raw JSON...............###
"""
    Save raw API response to a JSON file.
    Always save before transforming anything.

    data       : the raw JSON response from NVE
    station_id : used in the filename so you know
                 which station this file belongs to
"""
def save_raw(data,station_id):
    
    # Create a timestamp so every file has a unique name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Clean the station_id for use in filename
    # 12.228.0 becomes 12_228_0 (dots not allowed in filenames)
    clean_station_id = station_id.replace('.','_')
    
    # Create the filename
    file_name = f"extract/raw/discharge_{clean_station_id}_{timestamp}.json"
    
    # Write the data to the file
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f'Raw data saved: {file_name}')
    
    return file_name

if __name__ == "__main__":
    if API_read:
        print(f"The API Key is: {API_read[:6]}")
        print(f'The base api url is: {base_api_url}')
    else:
        print('There is an error! in .env')
    
    ##### for block-2 fetch dat.....   
    # Fetch real data — Kistefoss station, Randselva 
    # Parameter 1001 = river discharge in m³/s
    data = fetch_station(
        station_id= "12.228.0",
        parameter= '1001',
        resolution= '60',
        days_back= 3
    )
    
    #### for block-3 save data......
    file_name = save_raw(data, '12.228.0')
    
    # print the return values
    print(f'\nTop level keys: {list(data.keys())}')
    print(f'Item count: {data.get('itemCount')}')
    
    # First series
    first = data["data"][0]
    print(f"\nStation name : {first['stationName']}")
    print(f"Parameter    : {first['parameterNameEng']}")
    print(f"Unit         : {first['unit']}")
    print(f"Observations : {first['observationCount']}")

        # First 5 readings
    print(f"\nFirst 5 readings:")
    for obs in first["observations"][:5]:
        print(f"  {obs['time']}  "
                f"{obs['value']:.2f} m³/s  "
                f" correction: {obs['correction']} "
                f"quality: {obs['quality']}")