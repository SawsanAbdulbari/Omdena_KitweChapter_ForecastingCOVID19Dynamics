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
    
    # Take logarithm
    user_input, last_value = np.log(user_input), np.log(last_value)

    # Apply differencing
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
            if feature == "fullyVaccinated":
                input_data[feature] = st.number_input(f"Enter {feature}", min_value=9327654, step=1)
            elif feature == "partiallyVaccinated":
                input_data[feature] = st.number_input(f"Enter {feature}", min_value=4663827, step=1)
            elif feature == "totalVaccinations":
                input_data[feature] = st.number_input(f"Enter {feature}", min_value=9982068, step=1)
            elif feature in ["stringency_index", "positive_rate", "rfh", "r3h"]:
                input_data[feature] = st.number_input(f"Enter {feature}", min_value=0, step=0.001)
            elif feature == "day_of_week":
                input_data[feature] = st.number_input(f"Enter day of week (0 to 6)", min_value=0, max_value=6, step=1)
            elif feature == "month":
                input_data[feature] = st.number_input(f"Enter the month (1 to 12)", min_value=1, max_value=12, step=1)
            else:
                input_data[feature] = st.number_input(f"Enter {feature}", min_value=0, step=1)

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
