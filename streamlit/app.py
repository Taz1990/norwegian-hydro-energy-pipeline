import os
import psycopg2
import pandas as pd
import streamlit as st
from dotenv import dotenv_values

# Load Streamlit-specific .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
print("Loading .env from:", env_path)

env = dotenv_values(env_path)

# ---------- DB CONNECTION ----------
PG_HOST = env.get("PG_HOST")
PG_PORT = env.get("PG_PORT")
PG_DATABASE = env.get("PG_DATABASE")
PG_USER = env.get("PG_USER")
PG_PASSWORD = env.get("PG_PASSWORD")

print("PG_HOST =", PG_HOST)
print("PG_DATABASE =", PG_DATABASE)
print("PG_USER =", PG_USER)
print("PG_PASSWORD =", PG_PASSWORD)


@st.cache_data
def load_data():
    conn = psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

    query = """
        SELECT
            station_id,
            station_name,
            date,
            min_discharge,
            max_discharge,
            avg_discharge,
            measurements,
            discharge_trend
        FROM marts_hydro_metrics
        ORDER BY station_id, date;
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# ---------- STREAMLIT UI ----------
st.title("Norwegian Hydro Discharge Dashboard")

df = load_data()

if df.empty:
    st.warning("No data found in marts_hydro_metrics. Run Airflow + dbt first.")
else:
    stations = df["station_name"].unique()
    selected_station = st.selectbox("Select station", stations)

    station_df = df[df["station_name"] == selected_station]

    st.subheader(f"Daily discharge metrics for {selected_station}")

    latest = station_df.sort_values("date").iloc[-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest avg discharge", f"{latest['avg_discharge']:.2f}")
    col2.metric("Latest min discharge", f"{latest['min_discharge']:.2f}")
    col3.metric("Latest max discharge", f"{latest['max_discharge']:.2f}")

    st.line_chart(
        station_df.set_index("date")[["avg_discharge"]],
        use_container_width=True
    )

    st.subheader("Discharge trend (today vs yesterday)")
    st.line_chart(
        station_df.set_index("date")[["discharge_trend"]],
        use_container_width=True
    )

    st.subheader("Raw daily metrics")
    st.dataframe(station_df, use_container_width=True)
