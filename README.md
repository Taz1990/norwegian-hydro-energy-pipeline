# Norwegian Hydro-Energy Pipeline

An end-to-end ELT data engineering project that ingests real Norwegian hydrological data from NVE HydAPI, loads raw observations into PostgreSQL (acting as the analytical warehouse), transforms them with dbt, orchestrates workflows with Airflow and serves insights through a Streamlit dashboard. 

## Overview: 

Norway relies heavily on hydropower and river discharge is one of the most important indicators of water availability, reservoir inflow and hydropower production potential. In this project I have used real hydrological data to build a practical pipeline for collecting, transforming and visualizing discharge trends across five stations among 625 stations in Norway.

## Goal: 

The aim of this project is to demonstrate my core data engineering skills using a realistic data source and a production-style workflow: extraction, loading, transformation, orchestration, warehousing and visualization.

## Key Features:

- Extracts river discharge data from NVE HydAPI.
- Loads raw data into PostgreSQL running in Docker.
- Uses dbt for staging, core and mart-layer transformations.
- Orchestrates the pipeline with Apache Airflow.
- Serves the final data in an interactive Streamlit dashboard.
- Includes basic data quality checks such as unique and not_null.

## Architecture Diagram:

<img width="424" height="415" alt="image" src="https://github.com/user-attachments/assets/6354d7fa-2e64-4a96-8b31-38506ebc59d1" />

## Tech Stack:

- **Data Ingestion** — Python, requests, NVE HydAPI - Extract hydrological discharge data from the Norwegian Water Resources API
- **Storage** — PostgreSQL, Docker - Store raw, staging, core, and mart schemas in a containerized database
- **Transformation** — dbt, Jinja SQL models - Transform raw data into clean analytics tables with data quality tests
- **Orchestration** — Apache Airflow - Schedule and manage ETL tasks across extract, transform, and load stages
- **Processing & Serving** — Streamlit - Compute metrics and visualize trends through interactive dashboards

## Data Source:

- **NVE HydAPI** — River discharge (m³/s)
- **Frequency** — Hourly or daily depending on station

## Project Structure: 

### Raw layer:
Stores the API responses exactly as received.

### Staging layer:
Cleans and standardizes the raw observations.
- Deduplication
- Column renaming
- Basic validation

### Core Layer: 
Builds business ready tables such as:
- Daily discharge summaries
- Station level metrics

Creates dashboard ready tables:
- Trend indicators
- Aggregated metrics
- Station performance summaries

### dbt Models:

#### Staging Models:
- `stg_raw_discharge`
- `stg_stations`

#### Core Models:
- `core_daily_summary`

#### Mart Models:
- `marts_hydro_metrics`

These models support:
- Station level reporting
- Daily averages
- Min/max discharge values
- Trend calculations
- Dashboard metrics

## Streamlit Dashboard:

The dashboard includes:
- Station selector
- Latest daily metrics
- Average, minimum, and maximum discharge charts
- Trend indicator comparing today vs yesterday
- Raw data table
- Auto-refresh when the pipeline runs

## Workflow:

1. **Extract**  
   Airflow triggers a Python extraction job that calls the NVE HydAPI and saves the raw JSON observations exactly as received.

2. **Load**  
   Raw hydrological observations are inserted into PostgreSQL in the raw schema, forming the foundation for reproducible ELT processing.

3. **Transform**  
   dbt builds:
   - staging views (clean + standardized)
   - core summaries (daily discharge metrics)
   - mart tables (dashboard ready aggregates and trends)

4. **Serve**  
   Streamlit queries the mart layer and displays:
   - interactive line charts
   - daily metrics
   - trend indicators
   - raw data tables

## Setup: 

1. **Clone the repository**
   git clone [https://github.com/Taz1990/norwegian-hydro-energy-pipeline](https://github.com/Taz1990/norwegian-hydro-energy-pipeline) 
  - cd norwegian-hydro-energy-pipeline

3. Start Docker services
* docker-compose up –d

This launches:
	-	PostgreSQL
	-	Airflow scheduler 
	-	Airflow webserver 
	-	Airflow init container 
	
5. Access Airflow    
Open the UI: http://localhost:8080

7. Configure dbt    
Add PostgreSQL credentials to  .dbt/profiles.yml

9. Run the pipeline  
Trigger the DAG from the Airflow UI  
Airflow will orchestrate:  
	-	extract → transform → load → dbt
	
10. Start the dashboard   
* streamlit run streamlit/app.py

## Future Improvements:
	•	Integrate weather data such as precipitation and temperature. 
	•	Add water level data. 
	•	Deploy the pipeline to Azure. 

## Skills Demonstrated
	- **API ingestion** — Building Python clients to retrieve real time and historical hydrological data from REST APIs. 
	- **ELT pipeline design** — Designing modular extract  load  transform workflows using modern best practices. 
	- **SQL data modeling** — Structuring raw, staging, core and mart schemas for analytical workloads. 
	- **dbt transformations** — Implementing Jinja SQL models, staging views, core summaries and mart tables. 
	- **Airflow orchestration** — Scheduling and managing multi step ELT pipelines with task dependencies. 
	- **PostgreSQL warehousing** — Managing a containerized warehouse for raw and transformed hydrological data. 	
	- **Dockerized development** — Running Airflow, PostgreSQL and dbt in isolated, reproducible containers. 
	- **Streamlit dashboarding** — Building interactive dashboards with charts, metrics and trend indicators. 
	- **Working with real Norwegian hydrological data** — Handling real world environmental datasets from NVE HydAPI.

## Conclusion
This project demonstrates my practical data engineering skills through a complete pipeline built around real public data. It shows my experience with ingestion, loading, transformation, orchestration and visualization, making it a strong portfolio project for junior data engineering roles.



