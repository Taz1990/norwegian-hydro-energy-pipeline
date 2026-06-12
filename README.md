# Norwegian Hydro-Energy Pipeline

An end-to-end data pipeline that ingests real Norwegian 
hydrological and weather data and serves insights on a live dashboard.

## What it does
Collects river discharge and water level observations from 
NVE (Norwegian Water Resources and Energy Directorate) across 
Norway's key hydropower regions. Norway generates 90% of its 
electricity from hydropower — river discharge data directly 
reflects energy production capacity.

## Stack
- **Extract**: Python · requests · NVE HydAPI
- **Transform**: pandas · dbt
- **Load**: PostgreSQL · sqlalchemy  
- **Orchestration**: Apache Airflow
- **Processing**: PySpark
- **Dashboard**: Streamlit
- **Cloud**: Azure (Phase 2)

## Data Sources
| Source | Data | Update frequency |
|--------|------|-----------------|
| NVE HydAPI | River discharge · water levels | Hourly |
| Open-Meteo | Temperature · precipitation · wind | Hourly |

## Hydropower Regions
| Region | Zone | Key rivers |
|--------|------|-----------|
| East Norway | NO1 | Glomma, Drammenselva |
| South Norway | NO2 | Otra, Tovdalselva |
| Central Norway | NO3 | Orkla, Gaula |
| North Norway | NO4 | Målselva, Reisa |
| West Norway | NO5 | Vosso, Aurland |

## Project Status
🔨 In active development — Week 1 of 8

## Architecture
NVE HydAPI ──→ Python extract ──→ PostgreSQL raw
│
dbt models
│
PySpark jobs
│
Streamlit dashboard
