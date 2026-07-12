###########........A single pipeline.py file that ties together extract, transform & load for Airflow......#######
import logging
from extract.NVEapi import extract
from transform.clean import transform
from load.postgresql import load_to_postgresql
import os
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger=logging.getLogger(__name__)

######....Main pipeline function.....######
def run_pipeline(station_id:str, parameter:str, resolution:str, days_back:int):
    """
    Full ETL pipeline:
    1. Extract from API
    2. Transform DataFrame
    3. Load into PostgreSQL
    """
    """
    Dual-mode ETL pipeline:
    - Airflow mode: extract → file_name, transform → JSON, load → JSON
    - Local mode:   extract → df, file_name, transform → df, load → df
    """
    try:
        logger.info('Starting ETL Pipeline')
        logger.info(f'Extracting data for station_id= {station_id}, parameter= {parameter}')
        
        running_in_airflow = os.getenv("AIRFLOW__CORE__EXECUTOR") is not None
        #Extract
        extract_result = extract(
            station_id=station_id,
            parameter=parameter,
            resolution=resolution,
            days_back=days_back
        )
        if running_in_airflow:
            # Airflow: extract() returns only file_name
            file_name = extract_result
            logger.info(f"Extraction complete. Raw file saved: {file_name}")
        else:
            # Local: extract() returns (df, file_name)
            df, file_name = extract_result
            logger.info(f"Extraction complete. Raw file saved: {file_name}")
            logger.info(f"Extracted DataFrame shape: {df.shape}")
                    
        
        #Transform
        if running_in_airflow:
            clean_json = transform(file_name)
            logger.info("Transform complete. JSON returned for Airflow")
        else:
            clean_df = transform(df)
            logger.info(f"Transform complete. Clean DataFrame shape: {clean_df.shape}")
        
        #Load
        logger.info('Start loading into PostgreSQL')
        
        if running_in_airflow:
            inserted_rows = load_to_postgresql(clean_json)
        else:
            inserted_rows = load_to_postgresql(clean_df)   
        logger.info(f"Load complete. Inserted rows: {inserted_rows}")
        logger.info("ETL pipeline finished successfully")
                               
        return {
        'file_name': file_name,
        'rows_inserted': inserted_rows,
        "clean_df": None if running_in_airflow else clean_df 
        }
    
    except Exception as e:
        logger.info('Pipeline failed!!! Check for error')
        logger.exception(e)
        raise

if __name__ == "__main__":
    result = run_pipeline(
        station_id='12.228.0',
        parameter='1001',
        resolution= '60',
        days_back= 3
    )
    
    print(f"Inserted rows: {result['rows_inserted']}")
    print(result["clean_df"])