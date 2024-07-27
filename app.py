import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from streamlit_option_menu import option_menu
import os

# Generate example household data
@st.experimental_memo
def generate_household_data(start_date, end_date):
    np.random.seed(42)  # For reproducible results
    num_households = 100
    dates = pd.date_range(start=start_date, end=end_date)
    data = pd.DataFrame({
        'Household ID': np.arange(1, num_households + 1),
        'Ward': np.random.choice(['A', 'B', 'C', 'D'], size=num_households),
        'Area': np.random.choice(['Urban', 'Suburban', 'Rural'], size=num_households),
        'Monthly Water Usage (Liters)': np.random.rand(num_households) * 150,
        'Leakage Detected (Yes/No)': np.random.choice(['Yes', 'No'], size=num_households),
        'Disparity in Supply (Yes/No)': np.random.choice(['Yes', 'No'], size=num_households),
        'Income Level': np.random.choice(['Low', 'Medium', 'High'], size=num_households),
        'Household Size': np.random.randint(1, 6, size=num_households),
        'Date': np.random.choice(dates, size=num_households)
    })
    return data

# Load pre-trained model and preprocessor
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_model_and_preprocessor(model_file, preprocessor_file):
    try:
        model = tf.keras.models.load_model(model_file)
    except Exception as e:
        return None, None, f"Failed to load model: {str(e)}"
    
    try:
        preprocessor = joblib.load(preprocessor_file)
    except Exception as e:
        return None, None, f"Failed to load preprocessor: {str(e)}"

    return model, preprocessor, None

# Ensure preprocessor is fitted correctly before transforming data
@st.cache(allow_output_mutation=True)
def fit_preprocessor(preprocessor, data):
    features = data[['Ward', 'Area', 'Leakage Detected (Yes/No)', 'Disparity in Supply (Yes/No)', 'Income Level', 'Household Size']]
    preprocessor.fit(features)
    return preprocessor

# Navbar setup
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", "Data", "Model", "About"], 
        icons=['house', 'database', 'gear', 'info'], menu_icon="cast", default_index=0)

# Home page
if selected == "Home":
    st.title("Water Supply Management")
    st.write("Welcome to the Water Supply Management System. Use the sidebar to navigate to different sections.")

# Data page
elif selected == "Data":
    st.title("Data Overview")
    date_option = st.selectbox("Select date range", ["1 month", "6 months", "1 year"])

    if date_option == "1 month":
        start_date = datetime.now() - timedelta(days=30)
    elif date_option == "6 months":
        start_date = datetime.now() - timedelta(days=182)
    elif date_option == "1 year":
        start_date = datetime.now() - timedelta(days=365)

    end_date = datetime.now()

    # Update data based on selected date range
    if st.button("Update Data"):
        household_data = generate_household_data(start_date, end_date)
        st.write("### Household Data", household_data)

        # Calculate statistics
        total_households = len(household_data)
        households_receiving_water = household_data['Leakage Detected (Yes/No)'].value_counts().get('No', 0)
        households_not_receiving_water = total_households - households_receiving_water

        used_within_limit = (household_data['Monthly Water Usage (Liters)'] <= 100).sum()
        wasted_beyond_limit = (household_data['Monthly Water Usage (Liters)'] > 100).sum()

        total_usage = household_data['Monthly Water Usage (Liters)'].sum()
        total_wasted = household_data.loc[household_data['Monthly Water Usage (Liters)'] > 100, 'Monthly Water Usage (Liters)'].sum() - 100 * wasted_beyond_limit

        mean_usage = household_data['Monthly Water Usage (Liters)'].mean()
        median_usage = household_data['Monthly Water Usage (Liters)'].median()
        std_usage = household_data['Monthly Water Usage (Liters)'].std()

        st.write(f"*Total households*: {total_households}")
        st.write(f"*Households receiving water*: {households_receiving_water}")
        st.write(f"*Households not receiving water*: {households_not_receiving_water}")
        st.write(f"*Households using water within limit*: {used_within_limit}")
        st.write(f"*Households wasting water beyond limit*: {wasted_beyond_limit}")
        st.write(f"*Total water usage (liters)*: {total_usage:.2f}")
        st.write(f"*Total water wasted (liters)*: {total_wasted:.2f}")
        st.write(f"*Mean water usage (liters)*: {mean_usage:.2f}")
        st.write(f"*Median water usage (liters)*: {median_usage:.2f}")
        st.write(f"*Standard deviation of water usage (liters)*: {std_usage:.2f}")

        # Interactive bar plot
        fig = px.bar(
            x=['Receiving Water', 'Not Receiving Water'], 
            y=[households_receiving_water, households_not_receiving_water],
            labels={'x': 'Household Status', 'y': 'Number of Households'},
            title='Households Receiving vs. Not Receiving Water'
        )
        st.plotly_chart(fig)

        fig2 = px.bar(
            x=['Within Limit', 'Beyond Limit'], 
            y=[used_within_limit, wasted_beyond_limit],
            labels={'x': 'Usage Status', 'y': 'Number of Households'},
            title='Households Using Water Within Limit vs. Beyond Limit'
        )
        st.plotly_chart(fig2)

        # Heatmap for water usage
        heatmap_data = household_data.pivot_table(values='Monthly Water Usage (Liters)', index='Household ID', columns='Date', fill_value=0)
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        sns.heatmap(heatmap_data, ax=ax3, cmap='viridis')
        st.pyplot(fig3)

# Model page
elif selected == "Model":
    st.title("Model Training and Prediction")
    model_path = 'water_usage_model.h5'
    preprocessor_path = 'preprocessor.pkl'

    # File upload widgets
    model_file = st.file_uploader("Upload the model file (water_usage_model.h5)", type=["h5"])
    preprocessor_file = st.file_uploader("Upload the preprocessor file (preprocessor.pkl)", type=["pkl"])

    if model_file is not None:
        with open(model_path, "wb") as f:
            f.write(model_file.getbuffer())

    if preprocessor_file is not None:
        with open(preprocessor_path, "wb") as f:
            f.write(preprocessor_file.getbuffer())

    # Check if model and preprocessor files exist
    if not os.path.exists(model_path):
        st.error("Model file not found. Please upload the model file to the correct path.")
        st.stop()

    if not os.path.exists(preprocessor_path):
        st.error("Preprocessor file not found. Please upload the preprocessor file to the correct path.")
        st.stop()

    # Load pre-trained model and preprocessor
    model, preprocessor, error_message = load_model_and_preprocessor(model_path, preprocessor_path)
    if error_message:
        st.error(error_message)
        st.stop()

    # Ensure preprocessor is fitted correctly
    household_data = generate_household_data(datetime.now() - timedelta(days=365), datetime.now())
    preprocessor = fit_preprocessor(preprocessor, household_data)

    # Example of model prediction
    def predict_usage(model, data):
        # Select relevant features for prediction
        features = data[['Ward', 'Area', 'Leakage Detected (Yes/No)', 'Disparity in Supply (Yes/No)', 'Income Level', 'Household Size']]
        features = preprocessor.transform(features)
        prediction = model.predict(features)
        return prediction.flatten()

    if st.button("Predict Usage"):
        try:
            prediction = predict_usage(model, household_data)
            household_data['Predicted Usage'] = prediction

            st.write("### Predicted Data", household_data)

            # Debugging: Print shapes and first few rows of actual and predicted usage
            st.write("Shape of features:", household_data.shape)
            st.write("Shape of predictions:", prediction.shape)
            st.write("First few rows of actual usage:")
            st.write(household_data['Monthly Water Usage (Liters)'].head())
            st.write("First few rows of predicted usage:")
            st.write(prediction[:5])

            # Interactive plot for predictions
            fig4 = go.Figure()
            fig4.add_trace(go.Scatter(x=household_data['Household ID'], y=household_data['Monthly Water Usage (Liters)'], mode='lines', name='Actual'))
            fig4.add_trace(go.Scatter(x=household_data['Household ID'], y=household_data['Predicted Usage'], mode='lines', name='Predicted'))
            fig4.update_layout(title='Actual vs. Predicted Water Usage', xaxis_title='Household ID', yaxis_title='Water Usage (liters)')
            st.plotly_chart(fig4)

            # Saving data example
            if st.button("Save Data"):
                household_data.to_csv('predicted_household_water_usage.csv')
                st.write("Data saved to predicted_household_water_usage.csv")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

# About page
elif selected == "About":
    st.title("About")
    st.write("This application is designed to manage water supply for households. It provides data analysis and predictive modeling for water usage. The system can predict future water usage based on various factors such as household size, days without water, and average temperature. The data is visualized using interactive plots for better understanding and decision making.")
