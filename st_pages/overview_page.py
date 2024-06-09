import warnings
import pandas as pd
import streamlit as st
import plotly.express as px

warnings.filterwarnings('ignore')

def plot1(df):
    fig = px.line(df, x='Unnamed: 0', y='imputed_total_cases', 
                    labels={"Unnamed: 0": "Date", "imputed_total_cases": "Total Cases"},
                        title="COVID-19 Cases Over Time")
    
    fig.update_layout(
        autosize=True,
        height=250,
        margin=dict(l=0, r=0, t=25, b=10),
    )
        
    st.plotly_chart(fig, use_container_width=True)

def plot2(df):
    fig = px.line(df, x='Unnamed: 0', y='imputed_total_deaths', 
                    labels={"Unnamed: 0": "Date", "imputed_total_deaths": "Total Deaths"}, 
                        title="COVID-19 Deaths Over Time")
    fig.update_layout(
        autosize=True,
        height=250,
        margin=dict(l=0, r=0, t=25, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

def plot3(df):
    fig = px.line(df, x='Unnamed: 0', y='totalVaccinations', 
                    labels={"Unnamed: 0": "Date", "totalVaccinations": "Total Vaccinations"},
                    title="COVID-19 Vaccinations Over Time")
    fig.update_layout(
        autosize=True,
        height=250,
        margin=dict(l=0, r=0, t=25, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

overview = None

def main(overview):
    df = pd.read_csv("preprocessed_data_updated.csv")
    overview.write("<h3>📊 Overview Of COVID-19 Data</h3>", unsafe_allow_html=True)

    total_cases = df['imputed_total_cases'].sum()
    total_deaths = df['imputed_total_deaths'].sum()
    total_vaccinations = df['totalVaccinations'].sum()
    total_tests = df['totalTests'].sum()

    formatted_total_cases = f"{total_cases / 1e3:.1f} K"
    formatted_total_deaths = f"{total_deaths / 1e3:.1f} K"
    formatted_total_vaccinations = f"{total_vaccinations / 1e6:.1f} M"
    formatted_total_tests = f"{total_tests / 1e6:.1f} M"

    a1, a2, a3, a4, input_area, dl_csv = overview.columns([1,1,1,1,2,1.5])
    a1.metric("Total Cases", formatted_total_cases)
    a2.metric("Total Deaths", formatted_total_deaths)
    a3.metric("Total Vaccinations", formatted_total_vaccinations)
    a4.metric("Total Tests", formatted_total_tests)

    try:
        date_range = input_area.date_input(
            "Select Date Range",
            [pd.to_datetime(df["Unnamed: 0"]).min(), pd.to_datetime(df["Unnamed: 0"]).max()]
        )
        csv = df.to_csv(index=False).encode('utf-8')
        dl_csv.write("<br>"*1, unsafe_allow_html=True)
        dl_csv.download_button("Download Data", data=csv, file_name="covid_data.csv", mime="text/csv", use_container_width=True)
        
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        
        if start_date > end_date:
            overview.toast("Start date cannot be greater than end date.")

        df["Unnamed: 0"] = pd.to_datetime(df["Unnamed: 0"])
        df = df[(df["Unnamed: 0"] >= start_date) & (df["Unnamed: 0"] <= end_date)]

        if df.empty:
            overview.toast("No data found for the selected date range.")
        else:
            overview.dataframe(df, height=200)
            
        cols = overview.columns(3)
        
        with cols[0]:
            plot1(df)
        with cols[1]:
            plot2(df)
        with cols[2]:
            plot3(df)
            
    except IndexError:
        overview.dataframe(df, height=200)

if __name__ == '__main__':
    overview.set_page_config(page_title='COVID-19 Case Prediction App', page_icon='assets/img/favicon.png', layout='wide')
    main()