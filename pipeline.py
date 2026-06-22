###########........A single pipeline.py file that ties together extract, transform & load for Airflow......#######
import logging
from extract.NVEapi import extract
from transform.clean import transform
from load.postgresql import load_to_postgresql

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
    try:
        logger.info('Starting ETL Pipeline')
        logger.info(f'Extracting data for station_id= {station_id}, parameter= {parameter}')
        
        #Extract
        df, file_name = extract(
            station_id=station_id,
            parameter=parameter,
            resolution=resolution,
            days_back=days_back
        )
        logger.info(f'Extraction complete. Raw file saved{file_name}')
        logger.info(f"Extracted DataFrame shape: {df.shape}")
        
        #Transform
        logger.info('Starting Transform ')
        clean_df=transform(df)
        logger.info(f'Transform complete. Clean dataframe shape: {clean_df.shape}')
        
        #Load
        logger.info('Start loading into PostgreSQL')
        inserted_rows = load_to_postgresql(clean_df)
        logger.info(f'Load complete. Inserted rows: {inserted_rows}')
        
        logger.info("ETL pipeline finished successfully")
        
        return {
        'file_name': file_name,
        'clean_df': clean_df,
        'rows_inserted': inserted_rows 
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