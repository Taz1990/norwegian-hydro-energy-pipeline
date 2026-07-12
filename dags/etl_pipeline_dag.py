from airflow.exceptions import AirflowSkipException
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

# Import your ETL functions
from extract.NVEapi import extract
from transform.clean import transform
from load.postgresql import load_to_postgresql

# -------------------------
# WRAPPER FUNCTIONS
# -------------------------


def run_extract(**context):
    df_path = extract(
        station_id="12.228.0",
        parameter="1001",
        resolution="60",
        days_back=3
    )

    if df_path is None:
        raise AirflowSkipException("No data returned from API")

    return df_path


def run_transform(input_data):
    return transform(input_data)


def run_load(clean_json):
    return load_to_postgresql(clean_json)


# -------------------------
# DAG DEFINITION
# -------------------------

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
        python_callable=run_transform,
        op_args=["{{ ti.xcom_pull(task_ids='extract_task') }}"]
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=run_load,
        op_args=["{{ ti.xcom_pull(task_ids='transform_task') }}"]
    )

    dbt_run = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dbt && dbt run"
    )

    extract_task >> transform_task >> load_task >> dbt_run
