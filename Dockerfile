FROM apache/airflow:2.7.1-python3.11

USER airflow

# Install dbt inside Airflow's virtualenv
RUN pip install --user dbt-core dbt-postgres
