
import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
from datetime import datetime

# Load the model
model = load('../models/ridge_regression_model.pkl')

# Define helper functions
def validate_inputs(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):
    errors = []
    if not (-180.0 <= pickup_longitude <= 180.0):
        errors.append("Invalid pickup longitude.")
    if not (-90.0 <= pickup_latitude <= 90.0):
        errors.append("Invalid pickup latitude.")
    if not (-180.0 <= dropoff_longitude <= 180.0):
        errors.append("Invalid dropoff longitude.")
    if not (-90.0 <= dropoff_latitude <= 90.0):
        errors.append("Invalid dropoff latitude.")
    if passenger_count < 1:
        errors.append("Passenger count must be at least 1.")
    return errors

def calculate_distance(lat1, lon1, lat2, lon2):
    return np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)  # Placeholder, replace with accurate formula if needed

# Define airport coordinates
JFK_COORDINATES = (-73.8352, -73.7401, 40.6195, 40.6659)  # (lon_min, lon_max, lat_min, lat_max)
LGA_COORDINATES = (-73.8895, -73.8522, 40.7664, 40.7931)
EWR_COORDINATES = (-74.1925, -74.1594, 40.6700, 40.7081)

def check_airport_proximity(lon, lat, coordinates):
    lon_min, lon_max, lat_min, lat_max = coordinates
    in_lon_range = (lon_min <= lon) & (lon <= lon_max)
    in_lat_range = (lat_min <= lat) & (lat <= lat_max)
    return in_lon_range & in_lat_range

def prepare_data(input_features):
    input_features['hour'] = input_features['pickup_datetime'].dt.hour
    input_features['month'] = input_features['pickup_datetime'].dt.month
    input_features['dayofweek'] = input_features['pickup_datetime'].dt.dayofweek
    input_features['day'] = input_features['pickup_datetime'].dt.day
    input_features['distance_haversine'] = calculate_distance(
        input_features['pickup_latitude'], input_features['pickup_longitude'],
        input_features['dropoff_latitude'], input_features['dropoff_longitude']
    )
    input_features['distance_manhattan'] = (
        calculate_distance(input_features['pickup_latitude'], input_features['pickup_longitude'],
                        input_features['pickup_latitude'], input_features['dropoff_longitude']) +
        calculate_distance(input_features['pickup_latitude'], input_features['dropoff_longitude'],
                        input_features['dropoff_latitude'], input_features['dropoff_longitude'])
    )
    # Determine airport proximity
    input_features['pickup_jfk'] = check_airport_proximity(input_features['pickup_longitude'], input_features['pickup_latitude'], JFK_COORDINATES)
    input_features['pickup_lga'] = check_airport_proximity(input_features['pickup_longitude'], input_features['pickup_latitude'], LGA_COORDINATES)
    input_features['pickup_ewr'] = check_airport_proximity(input_features['pickup_longitude'], input_features['pickup_latitude'], EWR_COORDINATES)
    input_features['dropoff_jfk'] = check_airport_proximity(input_features['dropoff_longitude'], input_features['dropoff_latitude'], JFK_COORDINATES)
    input_features['dropoff_lga'] = check_airport_proximity(input_features['dropoff_longitude'], input_features['dropoff_latitude'], LGA_COORDINATES)
    input_features['dropoff_ewr'] = check_airport_proximity(input_features['dropoff_longitude'], input_features['dropoff_latitude'], EWR_COORDINATES)
    input_features['direction'] = np.arctan2(
        input_features['dropoff_longitude'] - input_features['pickup_longitude'],
        input_features['dropoff_latitude'] - input_features['pickup_latitude']
    )
    input_features['trip_speed'] = input_features['distance_haversine']  # Placeholder for actual speed calculation
    return input_features

# UI components
st.sidebar.image("img.png", caption='NYC Taxi', use_column_width=True)
st.sidebar.markdown("Made with :green_heart: by [Linda Marin](https://www.linkedin.com/in/lindamarin97/) & [Sawsan Abdulbari](https://www.linkedin.com/in/sawsanabdulbari/)")

st.title(':house_buildings: NYC Taxi Trip Duration Predictor')
st.write("This application predicts the taxi trip duration in NYC based on input features.")

# Form for input data
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        pickup_datetime = st.date_input('Pickup Date:', value=pd.to_datetime('today'))
        pickup_time = st.time_input('Pickup Time:', value=pd.to_datetime('now').time())
        pickup_longitude = st.number_input('Pickup Longitude:', -180.0, 180.0, value=-73.98)
        pickup_latitude = st.number_input('Pickup Latitude:', -90.0, 90.0, value=40.75)
        passenger_count = st.number_input('Passenger Count:', 1, 8, value=1)
    with col2:
        dropoff_longitude = st.number_input('Dropoff Longitude:', -180.0, 180.0, value=-73.98)
        dropoff_latitude = st.number_input('Dropoff Latitude:', -90.0, 90.0, value=40.75)
        vendor_id = st.selectbox('Vendor ID:', [1, 2])
        store_and_fwd_flag = st.selectbox('Store and Forward Flag:', ['N', 'Y'])

    submit_button = st.form_submit_button("Predict")

# Prediction handling
# Prediction handling
if submit_button:
    # Validate inputs
    errors = validate_inputs(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count)
    if errors:
        for error in errors:
            st.error(error)
    else:
        # Prepare the input features DataFrame
        input_features = pd.DataFrame({
            'pickup_datetime': [pd.to_datetime(str(pickup_datetime) + ' ' + str(pickup_time))],
            'pickup_longitude': [pickup_longitude],
            'pickup_latitude': [pickup_latitude],
            'dropoff_longitude': [dropoff_longitude],
            'dropoff_latitude': [dropoff_latitude],
            'passenger_count': [passenger_count],
            'vendor_id': [vendor_id],
            'store_and_fwd_flag': [store_and_fwd_flag]
        })

        # Add airport proximity, distance, and other required transformations
        input_features = prepare_data(input_features)
        
        # Predict using the model and display the result
        prediction = model.predict(input_features)[0]
        prediction_exp = np.expm1(prediction)  # Convert log output back to normal scale if applicable
        st.success(f'Estimated trip duration: {prediction_exp:.2f} minutes')


# Reset button
if st.button("Reset"):
    st.experimental_rerun()

# Footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
<div class="footer">
<p>Developed with <span style='color:red;'>❤</span> by <a href="https://www.linkedin.com/in/lindamarin97/" target="_blank">Linda Marin</a> & <a href="https://www.linkedin.com/in/sawsanabdulbari/" target="_blank">Sawsan Abdulbari</a></p>
</div>
""", unsafe_allow_html=True)