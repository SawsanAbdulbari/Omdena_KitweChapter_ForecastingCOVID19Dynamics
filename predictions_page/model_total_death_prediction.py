import pandas as pd
import streamlit as st
import numpy as np
from utils.preprocessing import preprocess_differencing, preprocess_log
from utils.model_loader import load_model_total_death

def total_death_prediction_page():
    st.title("COVID-19 Total Death Prediction :mask:")

    st.markdown("""
    ### Enter the required features to predict the total deaths from COVID-19.
    Please provide the values for the following features:
    """)
    st.write("**Note:** The minimum values for 'fullyVaccinated', 'partiallyVaccinated' and 'totalVaccinations' are the last known values as on 21st April 2024.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        
        imputed_active_cases = st.number_input("**imputed_active_cases**", min_value=0.0, help="Estimate of the number of active COVID-19 cases at a given time")
        fullyVaccinated = st.number_input("**fullyVaccinated**", min_value=9327654, value=9327654, step=1, help="Number of individuals who have completed the full vaccination regimen for COVID-19")
        new_vaccinations_smoothed = st.number_input("**new_vaccinations_smoothed**", min_value=0.0, help="New COVID-19 vaccination doses administered (7-day smoothed)")
        partiallyVaccinated = st.number_input("**partiallyVaccinated**", min_value=4663827, value=4663827, step=1, help="Number of individuals who have received at least one dose of a COVID-19 vaccine but have not yet completed the full vaccination regimen.")
        stringency_index = st.number_input("**stringency_index**", min_value=0.0, step=0.001, max_value=100.0, help="Government response composite measure based on 9 response indicators including school/workplace closures,and travel bans, value from 0 to 100(100=strictest)")
        test24hours = st.number_input("**test24hours**", min_value=0, help="Number of tests conducted in the last 24 hours")
        totalVaccinations = st.number_input("**totalVaccinations**", min_value=9982068, value=9982068, step=1, help="Total number of COVID-19 vaccination doses administered")

    with col2:  
        
        total_tests_per_thousand = st.number_input("**total_tests_per_thousand**", min_value=0.0, help="Total tests for COVID-19 per thousand people")
        vaccinated24hours = st.number_input("**vaccinated24hours**", min_value=0, help="Number of people vaccinated within a 24-hour period")
        positive_rate = st.number_input("**positive_rate**", min_value=0.0, step=0.001, help="Share of COVID-19 tests that are positive in a rolling 7-day average")
        rfh = st.number_input("**rfh**", min_value=0.0, step=0.001, help="10 day rainfall in mm")
        r3h = st.number_input("**r3h**", min_value=0.0, step=0.001, help="Rainfall 1-month rolling aggregation long term average in mm")
        month = st.number_input("**month**", min_value=1, max_value=12, help="The month in the year with January=1, December=12")
        day_of_week = st.number_input("**day_of_week**", min_value=0, max_value=6, help="The day of the week with Monday=0, Sunday=6")
        
    st.divider()

    input_df = pd.DataFrame({
            'imputed_active_cases': [imputed_active_cases],
            'fullyVaccinated': [fullyVaccinated],
            'new_vaccinations_smoothed': [new_vaccinations_smoothed],
            'partiallyVaccinated': [partiallyVaccinated],
            'stringency_index' : [stringency_index],
            'test24hours': [test24hours],
            'totalVaccinations': [totalVaccinations],
            'total_tests_per_thousand': [total_tests_per_thousand],
            'vaccinated24hours': [vaccinated24hours],
            'positive_rate': [positive_rate],
            'rfh': [rfh],
            'r3h': [r3h],
            'day_of_week': [day_of_week],
            'month':[month],
            })

    st.markdown("**Note:** The non-stationary features are differenced to make the data stationary.")

    differenced_features = {
        'fullyVaccinated': 9327654, 'partiallyVaccinated': 4663827, 'stringency_index': 13.89,
        'totalVaccinations': 9982068
    }

    log_feature = {'total_tests_per_thousand': 180}

    log_series = pd.Series(log_feature)

    differencing_data = pd.DataFrame([differenced_features])

    preprocessed_data = preprocess_differencing(input_df, differencing_data)

    for feature in log_feature.keys():
        preprocessed_data[feature] = preprocess_log(preprocessed_data[feature], log_series[feature])

    if st.button("Predict"):
        try:
            model = load_model_total_death()
            st.write("**You have submitted the below data.**")
            st.write(input_df)
            # prediction = predict_total_deaths(preprocessed_data)
            prediction = model.predict(preprocessed_data)
            st.success(f"Predicted Total Deaths: {prediction[0]: .3f}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
