import pandas as pd

# import numpy as np
# import pickle
import streamlit as st

# import xgboost as xgb
import joblib
import os

# Load the model
# @st.cache_resource
# def load_model(path):
#     with open(path, 'rb') as file:
#         model = pickle.load(file)
#     return model


# Define preprocessing function
def preprocess(main_dataframe, dataframe_with_last_known_value):
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
    common_columns = main_dataframe.columns.intersection(
        dataframe_with_last_known_value.columns
    )

    # Subtract the values of the known features
    for column in common_columns:
        main_dataframe[column] = (
            main_dataframe[column] - dataframe_with_last_known_value[column]
        )

    return main_dataframe


# Main function to display the Streamlit app
def main():
    st.title("COVID-19 Case Prediction :mask:")

    st.markdown(
        """
    ### Enter the required features to predict the total imputed COVID-19 cases.
    Please provide the values for the following features:
    """
    )

    # Input fields for each feature
    input_data = {}
    columns = st.columns(2)
    feature_list = [
        "fullyVaccinated",
        "new_deaths_smoothed",
        "new_people_vaccinated_smoothed",
        "new_vaccinations_smoothed",
        "partiallyVaccinated",
        "stringency_index",
        "test24hours",
        "totalTests",
        "totalVaccinations",
        "vaccinated24hours",
        "rfh",
        "r3h",
        "month",
        "day_of_week",
    ]

    info = [
        "Number of individuals who have completed the full vaccination regimen for COVID-19.",
        "New deaths attributed to COVID-19 (7-day smoothed). Counts can include probable deaths, where reported.",
        "Daily number of people receiving their first vaccine dose (7-day smoothed)",
        "New COVID-19 vaccination doses administered (7-day smoothed).",
        "Number of individuals who have received at least one dose of a COVID-19 vaccine but have not yet completed the full vaccination regimen.",
        "Government Response composite measure based on 9 response indicators including school/workplace closures, and travel bans, value from 0 to 100 (100 = strictest)",
        "Number of COVID-19 tests conducted within a 24-hour period.",
        "Total tests for COVID-19",
        "Total number of COVID-19 vaccine doses administered.",
        "Number of COVID-19 vaccine doses administered within a 24-hour period.",
        "rfh",
        "r3h",
        "Month",
        "Day of week",
    ]

    for i, feature in enumerate(feature_list):
        with columns[i % 2]:
            st.divider()
            st.caption(info[i])
            input_data[feature] = st.number_input(f"Enter {feature}", value=0)

    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])

    # Preprocess the input data
    differenced_features = {
        "fullyVaccinated": 9327654,
        "new_people_vaccinated_smoothed": 959,
        "partiallyVaccinated": 4663827,
        "stringency_index": 19.89,
        "totalTests": 4166833,
        "totalVaccinations": 9982068,
    }

    differencing_data = pd.DataFrame([differenced_features])

    preprocessed_data = preprocess(input_df, differencing_data)

    # Load the model
    model_path = "model/xgb_model_total_imputed_cases.pkl"

    if not os.path.exists(model_path):
        st.error(
            f" Model file not found at {model_path}. Please check the path and try again."
        )

    try:
        model = joblib.load(model_path)
    except Exception as e:
        st.error(f"An error occured while loading the model: {e}")
        return

    # Make prediction
    if st.button("Predict"):
        try:
            prediction = model.predict(preprocessed_data)
            st.success(f"Predicted Total Imputed Cases: {prediction[0]}")
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
