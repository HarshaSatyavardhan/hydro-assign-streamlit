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
    elif module == "Saturated Dissolved Oxygen":
        run_dissolved_oxygen_module()

def calculate_dissolved_oxygen(temperature,type):

    if(type == "1"):
        temperature = temperature.apply(lambda x: max(float(x), 1.0)) # Avoiding negative or zero temperatures for log
    else:
        temperature = max(float(temperature),1.0)
    temperature = temperature+273
    return (- 139.34 + ((1.575 * 10**5) / temperature) - 
            ((6.642308 * 10**7) / (temperature**2)) + 
            ((1.243800 * 10**10) / (temperature**3)) - 
            ((8.621949 * 10**11) / (temperature**4)))

def run_dissolved_oxygen_module():
    st.title("Saturated Dissolved Oxygen Calculator")

    # Sidebar to select option
    option = st.sidebar.radio("Select an option", ("Select Data", "Simulate Data"))

    if option == "Select Data":
        st.header("Select Data")
        st.write("Please upload an Excel/CSV file with river water temperature data.")

        # File upload for data selection
        uploaded_file = st.file_uploader("Upload Excel/CSV file", type=["xls", "xlsx", "csv"])

        if uploaded_file is not None:
            st.write("File Uploaded Successfully!")

            # Load data into a DataFrame
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(('.xls', '.xlsx')) else pd.read_csv(uploaded_file)

            # Display the loaded data
            st.write("Loaded Data:")
            st.write(df)

            # Calculate Saturated Dissolved Oxygen based on temperature
            df["Saturated Dissolved Oxygen"] = calculate_dissolved_oxygen(df["Temperature"],"1")

            # Display the calculated results
            st.write("Calculated Saturated Dissolved Oxygen:")
            st.write(df)

    elif option == "Simulate Data":
        st.header("Simulate Data")
        st.write("Please provide the river water temperature data.")

        # User input for temperature simulation
        temperature = st.number_input("Enter River Water Temperature", min_value=0.0, step=0.1)
        df = pd.read_csv("melted_data.csv")
        df["Saturated Dissolved Oxygen"] = calculate_dissolved_oxygen(df["Temperature"],"1")
        # Calculate Saturated Dissolved Oxygen based on provided temperature
        saturated_dissolved_oxygen = calculate_dissolved_oxygen(temperature,"2")

        # Display the calculated result
        st.write("Saturated Dissolved Oxygen:")
        st.write(saturated_dissolved_oxygen)

        # Display the calculated result
        st.write("Simulated Saturated Dissolved Oxygen:")
        st.write(df)



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
