"""To extract data from web API, download raw data, load api key"""

import requests
import  os
from dotenv import load_dotenv

load_dotenv() #to load the API key

API_read = os.getenv("NVE-API-KEY") #get API
#print(API_read)

#Base api url for observation dataset contains measured values
base_api_url = "https://hydapi.nve.no/api/v1/Observations"

#now check api & url
if __name__ == "__main__":
    if API_read:
        print(f"The API Key is: {API_read[:6]}")
        print(f"The base url is: {base_api_url}")
    else:
        print("Error! NO API found in .env")

