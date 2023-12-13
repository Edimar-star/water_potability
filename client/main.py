import streamlit as st
import requests
import os

def main():
    st.title("Water Potability Predictor")
    st.sidebar.header("Introduce los valores:")

    # Ejemplo potable
    ph = st.sidebar.slider("pH", 0.0, 15.0, 7.04)
    hardness = st.sidebar.slider("Hardness", 1.0, 300.0, 169.97)
    solids = st.sidebar.slider("Solids", 0.0, 45000.0, 23403.64)
    chloramines = st.sidebar.slider("Chloramines", 0.0, 15.0, 8.52)
    sulfate = st.sidebar.slider("Sulfate", 0.0, 500.0, 333.07)
    conductivity = st.sidebar.slider("Conductivity", 100.0, 1000.0, 475.57)
    organicCarbon = st.sidebar.slider("Organic Carbon", 1.0, 25.0, 12.92)
    trihalomethanes = st.sidebar.slider("Trihalomethanes", 0.0, 120.0, 50.86)
    turbidity = st.sidebar.slider("Turbidity", 1.0, 10.0, 2.75)

    # Botón para predecir la potabilidad
    st.write("""The Water Potability Predictor project aims to develop a predictive model that 
             assesses water quality and determines its potability. Water potability is a crucial 
             measure for public health, and having a system that can predict whether a water sample 
             is suitable for human consumption can be invaluable.""")
    if st.sidebar.button("predict potability"):
        potability = predict(ph, hardness, solids, chloramines, sulfate, conductivity, organicCarbon, trihalomethanes, turbidity)
        if potability == "Potable":
            st.success(f"Potability Result: {potability}")
        else:
            st.error(f"Potability Result: {potability}")

def predict(ph, hardness, solids, chloramines, sulfate, conductivity, organicCarbon, trihalomethanes, turbidity):
    url = os.getenv("URL")
    params = {
        "ph": ph,
        "Hardness": hardness,
        "Solids": solids,
        "Chloramines": chloramines,
        "Sulfate": sulfate,
        "Conductivity": conductivity,
        "OrganicCarbon": organicCarbon,
        "Trihalomethanes": trihalomethanes,
        "Turbidity": turbidity
    }

    response = requests.get(url, params=params)
    result = response.json()
    return result["message"] if "message" in result else result["Potability"]

if __name__ == "__main__":
    main()