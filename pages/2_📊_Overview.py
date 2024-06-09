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

st.title(":bar_chart: Overview Of COVID-19 Data")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


# Assuming your dataset is named 'covid_data.csv'
df = pd.read_csv("preprocessed_data_updated.csv")

# Display the first few rows of the dataset
# st.write(df.head())


# Calculate summary metrics
total_cases = df['imputed_total_cases'].sum()
total_deaths = df['imputed_total_deaths'].sum()
total_vaccinations = df['totalVaccinations'].sum()
total_tests = df['totalTests'].sum()

# Format the metrics for better readability
formatted_total_cases = f"{total_cases / 1e3:.1f} K"
formatted_total_deaths = f"{total_deaths / 1e3:.1f} K"
formatted_total_vaccinations = f"{total_vaccinations / 1e6:.1f} M"
formatted_total_tests = f"{total_tests / 1e6:.1f} M"

# Display the metrics in columns
a1, a2, a3, a4 = st.columns(4)
a1.metric("Total Cases", formatted_total_cases)
a2.metric("Total Deaths", formatted_total_deaths)
a3.metric("Total Vaccinations", formatted_total_vaccinations)
a4.metric("Total Tests", formatted_total_tests)


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
