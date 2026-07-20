from airflow.exceptions import AirflowSkipException
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import os

# Import ETL functions
from extract.NVEapi import extract
from transform.clean import transform
from load.postgresql import load_to_postgresql


# EXTRACT


def run_extract(**context):
    # Read stations from environment variable
    # if STATIONS is empty take it as a default station
    stations_env = os.getenv("STATIONS", "12.228.0:Kistefoss")
    stations = [s.split(":")[0] for s in stations_env.split(",")]

    results = []

    for station in stations:
        df_path = extract(
            station_id=station,
            parameter="1001",
            resolution="60",
            days_back=3
        )

        if df_path is None:
            print(f"No data for station {station}. Skipping.")
            continue

        results.append(df_path)

    if not results:
        raise AirflowSkipException("No data returned from API for any station")

    return results


# TRANSFORM

def run_transform(**context):
    # Pull list of raw file paths from extract_task
    input_paths = context['ti'].xcom_pull(task_ids='extract_task')

    clean_results = []

    for path in input_paths:
        clean_json = transform(path)
        clean_results.append(clean_json)

    return clean_results


# LOAD

def run_load(**context):
    clean_json_list = context['ti'].xcom_pull(task_ids='transform_task')

    for clean_json in clean_json_list:
        load_to_postgresql(clean_json)

    return "Load complete"

# DAG DEFINITION


with DAG(
    dag_id="hydro_etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["hydrology", "etl", "nve"]
):

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=run_extract
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=run_transform
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=run_load
    )

    dbt_run = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dbt && dbt run"
    )

    extract_task >> transform_task >> load_task >> dbt_run
