import pandas as pd
import streamlit as st
import numpy as np
import joblib
import os

# Define preprocessing function
def preprocess_differencing(main_dataframe, dataframe_with_last_known_value):

    # Identify the common columns
    common_columns = main_dataframe.columns.intersection(dataframe_with_last_known_value.columns)

    # Subtract the values of the known features
    for column in common_columns:
        main_dataframe[column] = main_dataframe[column] - dataframe_with_last_known_value[column]
        
    return main_dataframe

def preprocess_log(user_input, last_value):
    user_input, last_value = np.log(user_input), np.log(last_value)
    transformed_value = user_input - last_value
    return transformed_value
    
# Main function to display the Streamlit app
def main():
    st.title("COVID-19 Case Prediction :mask:")

    st.markdown("""
    ### Enter the required features to predict the total deaths from COVID-19.
    Please provide the values for the following features:
    """)

    # Input fields for each feature
    input_data = {}
    columns = st.columns(2)
    feature_list = [
        'imputed_active_cases', 'fullyVaccinated', 'new_vaccinations_smoothed', 
        'partiallyVaccinated', 'stringency_index', 'test24hours', 'totalVaccinations', 
        'total_tests_per_thousand', 'vaccinated24hours', 'positive_rate', 'rfh', 'r3h', 
        'day_of_week', 'month'
    ]
    
    for i, feature in enumerate(feature_list):
        with columns[i % 2]:
            input_data[feature] = st.number_input(f"Enter {feature}", value=0)

    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])

    # Preprocess the input data
    differenced_features = {
        'fullyVaccinated': 9327654, 'partiallyVaccinated': 4663827, 'stringency_index': 19.89, 
        'totalVaccinations': 9982068
    }

    log_feature = {'total_tests_per_thousand': 180}

    log_series = pd.Series(log_feature)

    differencing_data = pd.DataFrame([differenced_features])

    preprocessed_data = preprocess_differencing(input_df, differencing_data)

    for feature in log_feature.keys():
        preprocessed_data[feature] = preprocess_log(preprocessed_data[feature], log_series[feature])

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

    # Make prediction
    if st.button("Predict"):
        try:
            prediction = model.predict(preprocessed_data)
            st.success(f"Predicted Total Deaths: {prediction[0]}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
