import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import warnings
warnings.filterwarnings('ignore')
import base64
from typing import List

# Load external CSS
with open('./frontend/streamlit.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title(":bar_chart: Overview Of COVID-19 Data")

# Assuming your dataset is named 'covid_data.csv'
df = pd.read_csv("./data/preprocessed_data_updated.csv")
#Renaming the column name "Unnamed: 0" to "date"
df.rename(columns={"Unnamed: 0":"date"},inplace=True)
#Casting the date column into datetime type
df["date"] = pd.to_datetime(df["date"])

# Sidebar for additional information
st.sidebar.title('COVID-19 Dashboard')
st.sidebar.image("./media/omdena_zambia_highres.png", use_column_width='always') 
st.sidebar.write("This dashboard provides an overview of COVID-19 data, including cases, deaths, vaccinations, and testing trends.")
st.sidebar.divider()

# Filter options
st.sidebar.header("Filter Options")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[df["date"].min(), df["date"].max()], 
    min_value = df["date"].min(), 
    max_value = df["date"].max(),
    format = "MM/DD/YYYY",
)

# Ensure date_range is a tuple of start and end date
if len(date_range) == 2:
    start_date, end_date = date_range
    # Convert start_date and end_date to datetime64 if they are not already
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # Filter the DataFrame based on the selected date range
    filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
else:
    # If date_range is not a tuple of start and end date, use the entire DataFrame
    filtered_df = df

st.markdown('<style>div.block-container{padding-top:3rem;color:white}</style>', unsafe_allow_html=True)

# Calculate summary metrics
total_cases = filtered_df['imputed_total_cases'].max()
total_deaths = filtered_df['imputed_total_deaths'].max()
total_vaccinations = filtered_df['totalVaccinations'].max()
total_tests = filtered_df['totalTests'].max()
total_recoveries = filtered_df['imputed_total_recoveries'].max()

# Format the metrics for better readability
formatted_total_cases = f"{total_cases / 1e3:.1f} K"
formatted_total_deaths = f"{total_deaths / 1e3:.1f} K"
formatted_total_vaccinations = f"{total_vaccinations / 1e6:.1f} M"
formatted_total_tests = f"{total_tests / 1e6:.1f} M"
formatted_total_recoveries = f"{total_recoveries / 1e3:.1f} K"

titles = ["Total Cases", "Total Deaths", "Total Vaccinations", "Total Tests", "Total Recoveries"]
formatted_values = [formatted_total_cases, formatted_total_deaths,formatted_total_vaccinations,formatted_total_tests, formatted_total_recoveries]
values = [total_cases, total_deaths, total_vaccinations, total_tests]

# Function to display KPI metrics with custom styling
def display_kpi_metrics(kpis: List[float], kpi_names: List[str], bg_classes: List[str]):
    cols = st.columns(len(kpis))  # Create columns based on the number of KPIs
    for col, kpi_name, kpi_value, bg_class in zip(cols, kpi_names, kpis, bg_classes):
        col.markdown(f"""
            <div class="metric-container {bg_class}">
                <p>{kpi_value}</p>
                <h3>{kpi_name}</h3>
            </div>
        """, unsafe_allow_html=True)

bg_colors = ["bg-color-1", "bg-color-2", "bg-color-3", "bg-color-4", "bg-color-5"]

# First row with 2 columns
display_kpi_metrics(formatted_values[:2], titles[:2], bg_colors[:2])

# Second row with 3 columns
display_kpi_metrics(formatted_values[2:6], titles[2:6], bg_colors[2:6])

st.info(f"*The metrics displayed above is for the period {date_range}*")
st.divider()
# Visualization: Cases Over Time
st.subheader("COVID-19 Cases Over Time")
fig1 = px.line(filtered_df, x='date', y='imputed_total_cases', labels={"date": "Date", "imputed_total_cases": "Total Cases"})
st.plotly_chart(fig1, use_container_width=True)

# Visualization: Deaths Over Time
st.subheader("COVID-19 Deaths Over Time")
fig2 = px.line(filtered_df, x='date', y='imputed_total_deaths', labels={"date": "Date", "imputed_total_deaths": "Total Deaths"})
st.plotly_chart(fig2, use_container_width=True)



# Visualization: Vaccinations Over Time
st.subheader("COVID-19 Vaccinations Over Time")
fig3 = px.line(filtered_df, x='date', y='totalVaccinations', labels={"date": "Date", "totalVaccinations": "Total Vaccinations"})
st.plotly_chart(fig3, use_container_width=True)


# View and download data
st.subheader("View and Download Data")
with st.expander("**View Data**"):
    st.write(filtered_df.reset_index(drop=True))

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("**Download Data**", data=csv, file_name="covid_data.csv", mime="text/csv")



