import streamlit as st
import pandas as pd
import json
import requests

# Dummy Data for Demo (Replace these with real source data)
dummy_air_temp_data = [20, 21, 22, 23, 24, 25]
dummy_river_temp_data = [18, 19, 20, 21, 22, 23]

def main():
    st.title("River Water Quality Prediction Tool")

    module = st.sidebar.selectbox("Select Module", ["River Water Temperature", "Saturated Dissolved Oxygen"])

    if module == "River Water Temperature":
        run_river_water_temperature_module()

def run_river_water_temperature_module():
    st.header("River Water Temperature Prediction")

    air_temp = st.selectbox("Select Air Temperature", dummy_air_temp_data)
    river_temp = st.selectbox("Select Observed River Temperature", dummy_river_temp_data)
    model_type = st.selectbox("Select Model", ["Linear Regression", "Random Forest"])
    metric = st.selectbox("Select Performance Metric", ["RMSE", "MAE", "MSE"])

    if st.button("Submit"):
        # Prepare the data to send as JSON
        data = {
            "air_temperature": air_temp,
            "river_temperature": river_temp,
            "model_type": model_type,
            "metric": metric
        }

        # Fetch data from FastAPI backend
        response = requests.post("https://team2-hydro.onrender.com/predict/", json=data)

        if response.status_code == 200:
            result = response.json()
            st.write(f"Predicted River Temperature: {result['predicted_value']}")

            # Option to download the output in Excel/CSV
            download_data = {"Predicted Value": [result['predicted_value']]}
            df_download = pd.DataFrame(download_data)
            csv = df_download.to_csv(index=False)
            st.download_button(
                label="Download CSV File",
                data=csv,
                file_name='predicted_river_temperature.csv',
                mime='text/csv',
            )

        else:
            st.write("An error occurred during prediction.")

if __name__ == "__main__":
    main()
