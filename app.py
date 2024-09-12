import os
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from datetime import datetime, timedelta
from pycaret.regression import setup, compare_models, pull, save_model, load_model, predict_model

# Paths to model, scaler, and feature names
model_path = r'water_usage_model.h5'
scaler_path = r'scaler.pkl'
feature_names_path = r'feature_names.pkl'

# Load the trained model, scaler, and feature names
@st.cache_resource
def load_keras_model():
    try:
        model = tf.keras.models.load_model(model_path)
        scaler = joblib.load(scaler_path)
        feature_names = joblib.load(feature_names_path)
        return model, scaler, feature_names
    except Exception as e:
        st.error(f"Error loading Keras model or scaler: {e}")
        return None, None, None

model, scaler, feature_names = load_keras_model()

# Function to generate synthetic data
def generate_synthetic_data(num_records):
    data = {
        'Household ID': np.random.randint(1, 1000000, size=num_records),
        'Ward': np.random.randint(1, 50, size=num_records),
        'Area': np.random.randint(1, 100, size=num_records),
        'Leakage Detected (Yes/No)': np.random.choice([0, 1], size=num_records, p=[0.9, 0.1]),
        'Disparity in Supply (Yes/No)': np.random.choice([0, 1], size=num_records, p=[0.95, 0.05]),
        'Income Level': np.random.choice([0, 1, 2], size=num_records, p=[0.3, 0.5, 0.2]),
        'Household Size': np.random.randint(1, 10, size=num_records),
        'Monthly Water Usage (Liters)': np.random.randint(1000, 3000, size=num_records),
        'Date': [datetime.now() - timedelta(days=i) for i in range(num_records)]
    }
    return pd.DataFrame(data)

# PyCaret setup function
def setup_pycaret(df):
    try:
        st.write("Setting up PyCaret environment...")
        regression_setup = setup(data=df, target='Monthly Water Usage (Liters)', silent=True, session_id=123)
        st.success("PyCaret setup complete!")
        return regression_setup
    except Exception as e:
        st.error(f"Error setting up PyCaret environment: {e}")
        return None

# Function to train and compare models using PyCaret
def train_and_compare_models():
    try:
        st.write("Training models using PyCaret...")
        best_model = compare_models()
        st.write("Best Model: ", best_model)
        model_results = pull()
        st.dataframe(model_results)
        save_model(best_model, 'best_model_pycaret')
        st.success("Model training and comparison complete. Model saved successfully.")
    except Exception as e:
        st.error(f"Error training models: {e}")

# Streamlit layout
st.title("Water Usage Monitoring and Prediction")

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Generate & Predict", "Load & Retrain", "Interactive Plot"])

with tab1:
    if st.button("Generate Data and Predict"):
        num_records = st.slider("Number of records to generate", 1000, 10000, 10000)
        df = generate_synthetic_data(num_records)
        regression_setup = setup_pycaret(df)
        if regression_setup:
            train_and_compare_models()
            predict_and_analyze(df)
            generate_reports(df)

with tab2:
    uploaded_file = st.file_uploader("Choose a CSV file to retrain the model", type="csv")
    if uploaded_file:
        new_data = pd.read_csv(uploaded_file)
        retrain_model(new_data)

with tab3:
    if st.button("Generate Interactive Plot"):
        df = generate_synthetic_data(100)
        interactive_plot(df)
