import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from pycaret.classification import setup, compare_models, pull, save_model, load_model
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Load the dataset
file_path = 'indore_water_usage_data_difficult2.parquet'
household_data = pd.read_parquet(file_path)

# Map Section
st.title('Interactive Map Visualization')

if st.checkbox('Show Heat Map'):
    # Check if the dataset has latitude and longitude
    if 'latitude' in household_data.columns and 'longitude' in household_data.columns:
        # Filter data to get coordinates for heatmap
        map_data = household_data[['latitude', 'longitude']].dropna()
        # Initialize the map centered around the average coordinates
        m = folium.Map(location=[map_data['latitude'].mean(), map_data['longitude'].mean()], zoom_start=12)

        # Add the HeatMap layer
        HeatMap(data=map_data[['latitude', 'longitude']].values, radius=15, max_zoom=13).add_to(m)

        # Display the map
        folium_static(m)
    else:
        st.warning('Latitude and Longitude columns are required to generate a heat map.')

# Other PyCaret functionalities...
# PyCaret setup
if st.sidebar.checkbox('Setup PyCaret Environment'):
    target_variable = st.sidebar.selectbox('Select Target Variable', household_data.columns)
    if target_variable:
        pycaret_setup = setup(data=household_data, target=target_variable, silent=True, session_id=123)
        st.write('PyCaret environment setup complete.')

# Train and compare models
if st.sidebar.button('Train Models'):
    with st.spinner('Training models...'):
        best_model = compare_models()
        st.write('Best Model:', best_model)
        model_results = pull()
        st.dataframe(model_results)

        # Save the model
        save_model(best_model, 'best_model_pycaret')

# Load a saved model for prediction
if st.sidebar.checkbox('Load Model for Prediction'):
    model = load_model('best_model_pycaret')
    st.write('Model loaded successfully.')

    # Make predictions
    user_input = st.text_input('Enter new data for prediction (comma-separated values)')
    if user_input:
        data = pd.DataFrame([list(map(float, user_input.split(',')))], columns=household_data.columns[:-1])
        prediction = model.predict(data)
        st.write('Prediction:', prediction)
