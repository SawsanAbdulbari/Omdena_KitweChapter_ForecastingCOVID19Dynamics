import os
import pickle
import joblib
import pandas as pd
import streamlit as st
# import xgboost as xgb

model_path = './model/xgb_model_total_imputed_cases.pkl'

# Load the model
@st.cache_resource
def load_model(path):
    with open(path, 'rb') as file:
        model = pickle.load(file)
    return model

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
    common_columns = main_dataframe.columns.intersection(dataframe_with_last_known_value.columns)

    # Subtract the values of the known features
    for column in common_columns:
        main_dataframe[column] = main_dataframe[column] - dataframe_with_last_known_value[column]
        
    return main_dataframe

# Main function to display the Streamlit app
def main(mod):
    mod.write("<h3>😷 COVID-19 Case Prediction</h3>", unsafe_allow_html=True)
    mod.markdown("""
    ### Enter the required features to predict the total imputed COVID-19 cases.
    Please provide the values for the following features:
    """)

    input_data = {}
    columns = mod.columns(2)
    feature_list = [
        'fullyVaccinated', 'new_deaths_smoothed', 'new_people_vaccinated_smoothed', 
        'new_vaccinations_smoothed', 'partiallyVaccinated', 'stringency_index', 
        'test24hours', 'totalTests', 'totalVaccinations', 'vaccinated24hours', 
        'rfh', 'r3h', 'month', 'day_of_week'
    ]
    
    for i, feature in enumerate(feature_list):
        with columns[i % 2]:
            input_data[feature] = st.number_input(f"Enter {feature}", value=0)

    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])

    # Preprocess the input data
    differenced_features = {
        'fullyVaccinated': 9327654, 'new_people_vaccinated_smoothed': 959,
        'partiallyVaccinated': 4663827, 'stringency_index': 19.89, 'totalTests': 4166833, 'totalVaccinations': 9982068
    }

    differencing_data = pd.DataFrame([differenced_features])

    preprocessed_data = preprocess(input_df, differencing_data)

    if not os.path.exists(model_path):
        mod.error(f" Model file not found at {model_path}. Please check the path and try again.")
        return
    
    try:
        model = joblib.load(model_path)
    except Exception as e:
        mod.error(f"An error occured while loading the model: {e}")
        return

    # Make prediction
    with mod.columns(4)[-1]:
        predict_button = st.button("Predict", use_container_width=True)
    
    if predict_button:
        try:
            prediction = model.predict(preprocessed_data)
            mod.success(f"Predicted Total Imputed Cases: {prediction[0]}")
        except Exception as e:
            mod.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(st)