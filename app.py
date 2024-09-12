import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from pycaret.classification import setup, compare_models, pull, save_model, load_model
from streamlit_option_menu import option_menu

# Load the dataset
file_path = 'indore_water_usage_data_difficult2.parquet'
household_data = pd.read_parquet(file_path)

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
