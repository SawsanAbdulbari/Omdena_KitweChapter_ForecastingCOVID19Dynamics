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

st.markdown('<style>div.block-container{padding-top:3rem;color:white}</style>', unsafe_allow_html=True)

# Assuming your dataset is named 'covid_data.csv'
df = pd.read_csv("preprocessed_data_updated.csv")

# Calculate summary metrics
total_cases = df['imputed_total_cases'].max()
total_deaths = df['imputed_total_deaths'].max()
total_vaccinations = df['totalVaccinations'].max()
total_tests = df['totalTests'].max()
total_recoveries = df['imputed_total_recoveries'].max()

# Format the metrics for better readability
formatted_total_cases = f"{total_cases / 1e3:.1f} K"
formatted_total_deaths = f"{total_deaths / 1e3:.1f} K"
formatted_total_vaccinations = f"{total_vaccinations / 1e6:.1f} M"
formatted_total_tests = f"{total_tests / 1e6:.1f} M"
formatted_total_recoveries = f"{total_recoveries / 1e3:.1f} K"


# Display the metrics in columns
# a1, a2, a3, a4 = st.columns(4)
# a1.metric("Total Cases", formatted_total_cases)
# a2.metric("Total Deaths", formatted_total_deaths)
# a3.metric("Total Vaccinations", formatted_total_vaccinations)
# a4.metric("Total Tests", formatted_total_tests)

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

# Sidebar for additional information
st.sidebar.title('COVID-19 Dashboard')

# Add a logo to the sidebar
logo_path = "logo.jpg"
st.sidebar.image(logo_path, use_column_width=True)

st.sidebar.write("This dashboard provides an overview of COVID-19 data, including cases, deaths, vaccinations, and testing trends.")

# Filter options
st.sidebar.header("Filter Options")
# Date range filter
# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range", 
    [pd.to_datetime(df["Unnamed: 0"]).min(), pd.to_datetime(df["Unnamed: 0"]).max()]
)

# Convert date_range to datetime
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

df["Unnamed: 0"] = pd.to_datetime(df["Unnamed: 0"])
df = df[(df["Unnamed: 0"] >= start_date) & (df["Unnamed: 0"] <= end_date)]

# Display the first few rows of the filtered dataset to ensure the filter is applied correctly
st.write(df.head())

# Visualization: Cases Over Time
st.subheader("COVID-19 Cases Over Time")
fig1 = px.line(df, x='Unnamed: 0', y='imputed_total_cases', labels={"Unnamed: 0": "Date", "imputed_total_cases": "Total Cases"})
st.plotly_chart(fig1, use_container_width=True)

# Visualization: Deaths Over Time
st.subheader("COVID-19 Deaths Over Time")
fig2 = px.line(df, x='Unnamed: 0', y='imputed_total_deaths', labels={"Unnamed: 0": "Date", "imputed_total_deaths": "Total Deaths"})
st.plotly_chart(fig2, use_container_width=True)



# Visualization: Vaccinations Over Time
st.subheader("COVID-19 Vaccinations Over Time")
fig3 = px.line(df, x='Unnamed: 0', y='totalVaccinations', labels={"Unnamed: 0": "Date", "totalVaccinations": "Total Vaccinations"})
st.plotly_chart(fig3, use_container_width=True)


# View and download data
st.subheader("View and Download Data")
with st.expander("View Data"):
    st.write(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", data=csv, file_name="covid_data.csv", mime="text/csv")



