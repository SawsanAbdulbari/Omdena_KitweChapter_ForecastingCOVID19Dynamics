import pandas as pd
import numpy as np
import pickle
import streamlit as st
import xgboost as xgb

# Load the model
@st.cache_resource
def load_model(path):
    with open(path, 'rb') as file:
        model = pickle.load(file)
    return model

# Define preprocessing function
def preprocess(data, differenced_features):
    for feature in differenced_features:
        data[feature] = data[feature].diff().fillna(0)
    return data

# Main function to display the Streamlit app
def main():
    st.title("COVID-19 Case Prediction :mask:")

    st.markdown("""
    ### Enter the required features to predict the total imputed COVID-19 cases.
    Please provide the values for the following features:
    """)

    # Input fields for each feature
    input_data = {}
    columns = st.columns(2)
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
    differenced_features = [
        'fullyVaccinated', 'new_people_vaccinated_smoothed',
        'partiallyVaccinated', 'stringency_index', 'totalTests', 'totalVaccinations'
    ]
    preprocessed_data = preprocess(input_df, differenced_features)

    # Load the model
    model_path = '../model/xgb_model_total_imputed_cases.pkl'
    model = load_model(model_path)

    # Make prediction
    if st.button("Predict"):
        try:
            prediction = model.predict(preprocessed_data)
            st.success(f"Predicted Total Imputed Cases: {prediction[0]}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
