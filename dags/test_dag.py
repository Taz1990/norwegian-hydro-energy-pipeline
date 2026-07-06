from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello():
    print("Hello from Airflow!")

with DAG(
    dag_id="test_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
):
    task = PythonOperator(
        task_id="hello_task",
        python_callable=hello
    )
