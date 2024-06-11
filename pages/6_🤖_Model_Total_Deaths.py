import pandas as pd
import streamlit as st
import numpy as np
import joblib
import os

# Define preprocessing function
def preprocess_differencing(main_dataframe, dataframe_with_last_known_value):
    """
    Preprocess the main dataframe by subtracting values from the dataframe_with_last_known_value.

    Parameters:
    main_dataframe (pd.DataFrame): The main dataframe containing 14 features. 
                                   This dataframe is expected to have one row of user input.
    dataframe_with_last_known_value (pd.DataFrame): The dataframe containing 6 features and their known values.
                                                    This dataframe is expected to have one row with known values.

    Returns:
    pd.DataFrame: A new dataframe with the same structure as the main_dataframe, 
                  where the values of the 6 matching features have been subtracted 
                  by their corresponding values in the dataframe_with_last_known_value.
    """
    # Identify the common columns
    common_columns = main_dataframe.columns.intersection(dataframe_with_last_known_value.columns)

    # Subtract the values of the known features
    for column in common_columns:
        main_dataframe[column] = main_dataframe[column] - dataframe_with_last_known_value[column]
        
    return main_dataframe

def preprocess_log(user_input, last_value):
    '''
    Preprocess a feature by taking a logarithm from the user's input and the last known value and then subtracting
    the last known value from the user's input.

    Parameters:
    user_input (pd.Series): The series containing one value which is user's input.
                            The series expects to have only one value.
    last_value (pd.Series): The series containing one value which is the last known value.
                            The series expects to have only one value.

    Returns:
    pd.Series: A new series with one preprocessed value.
    '''

    # Use np.log1p for safer logarithm calculation
    log_user_input = np.log1p(user_input)
    log_last_value = np.log1p(last_value)

    # Apply differencing
    transformed_value = log_user_input - log_last_value

    return transformed_value

@st.cache_resource
def load_model():
# Load the model
    model_path = 'model/xgb_model_total_deaths.pkl'

    if not os.path.exists(model_path):
        st.error(f" Model file not found at {model_path}. Please check the path and try again.")
        return
    
    try:
        model = joblib.load(model_path)
    except Exception as e:
        st.error(f"An error occured while loading the model: {e}")
        return
    return model
    
# Main function to display the Streamlit app
def main():
    st.title("COVID-19 Case Prediction :mask:")

    st.markdown("""
    ### Enter the required features to predict the total deaths from COVID-19.
    Please provide the values for the following features:
    """)
    st.write("**Note:** The minimum values for 'fullyVaccinated', 'partiallyVaccinated' and 'totalVaccinations' are the last known values as on 21st April 2024.")

    st.divider()

    # Input fields for each feature
    
    col1, col2 = st.columns(2)
    feature_list = [
        'imputed_active_cases', 'fullyVaccinated', 'new_vaccinations_smoothed', 
        'partiallyVaccinated', 'stringency_index', 'test24hours', 'totalVaccinations', 
        'total_tests_per_thousand', 'vaccinated24hours', 'positive_rate', 'rfh', 'r3h', 
        'day_of_week', 'month'
    ]
    
    with col1:
        
        imputed_active_cases = st.number_input("**imputed_active_cases**", min_value=0.0, help="Estimate of the number of active COVID-19 cases at a given time")
        fullyVaccinated = st.number_input("**fullyVaccinated**", min_value=9327654, step=1, help="Number of individuals who have completed the full vaccination regimen for COVID-19")
        new_vaccinations_smoothed = st.number_input("**new_vaccinations_smoothed**", min_value=0.0, help="New COVID-19 vaccination doses administered (7-day smoothed)")
        partiallyVaccinated = st.number_input("**partiallyVaccinated**", min_value=4663827, step=1, help="Number of individuals who have received at least one dose of a COVID-19 vaccine but have not yet completed the full vaccination regimen.")
        stringency_index = st.number_input("**stringency_index**", min_value=0.0, step=0.001, max_value=100.0, help="Government response composite measure based on 9 response indicators including school/workplace closures,and travel bans, value from 0 to 100(100=strictest)")
        test24hours = st.number_input("**test24hours**", min_value=0, help="Number of tests conducted in the last 24 hours")
        totalVaccinations = st.number_input("**totalVaccinations**", min_value=9982068, step=1, help="Total number of COVID-19 vaccination doses administered")

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

    # Preprocess the input data
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

    # Make prediction
    if st.button("Predict"):
        try:
            model = load_model()
            st.write("**You have submitted the below data.**")
            st.write(input_df)
            prediction = model.predict(preprocessed_data)
            st.success(f"Predicted Total Deaths: {prediction[0]: .3f}") #Display the results upto three decimal places
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
