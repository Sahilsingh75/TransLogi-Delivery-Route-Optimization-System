#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import requests

# Load Delhi places data
delhi_places = pd.read_csv("delhi_places.csv")
place_names = delhi_places["Place Name"].tolist()

# FastAPI Endpoints
DELIVERY_TIME_API = "http://127.0.0.1:8000/predict_delivery_time/"
ROUTE_OPTIMIZATION_API = "http://127.0.0.1:8000/optimize_routes/"

# Streamlit UI
st.title("🚚 Delivery Route Optimization")

# Select Pickup Location
pickup = st.selectbox("Select Pickup Location", place_names)

# Select Delivery Location for Time Prediction
st.subheader("📦 Predict Delivery Time")
destination = st.selectbox("Select Delivery Location", place_names, key="delivery_location")
weight = st.number_input("Enter Order Weight (kg)", min_value=0.1, step=0.1, key="weight")

# Button for Delivery Time Prediction
if st.button("Predict Delivery Time"):
    if not pickup or not destination or not weight:
        st.error("Please fill all fields.")
    else:
        payload = {
            "pickup_location": pickup,
            "delivery_location": destination,
            "order_weight": weight
        }
        try:
            response = requests.post(DELIVERY_TIME_API, json=payload)
            response_data = response.json()

            if "detail" in response_data:
                st.error(response_data["detail"])
            else:
                st.success(f"**Predicted Delivery Time:** {response_data['predicted_delivery_time']} mins")
                st.info(f"Distance: {response_data['distance_km']} km")
                st.info(f"Traffic Duration: {response_data['traffic_duration_min']} mins")
                st.info(f"Weather: {response_data['weather_condition']} ({response_data['temperature_c']} °C)")
        except requests.RequestException as e:
            st.error(f"Failed to connect to API. {str(e)}")

# Route Optimization Section
st.subheader("🛣️ Optimize Delivery Routes")
destinations = st.text_area("Enter Delivery Locations (one per line)").split("\n")

# Button for Route Optimization
if st.button("Optimize Routes"):
    if not pickup or not destinations:
        st.error("Please fill all fields.")
    else:
        payload = {
            "pickup_location": pickup,
            "delivery_locations": destinations
        }
        try:
            response = requests.post(ROUTE_OPTIMIZATION_API, json=payload)
            response_data = response.json()

            if "detail" in response_data:
                st.error(response_data["detail"])
            else:
                st.success("Optimized Route:")
                st.write(" -> ".join(response_data['optimized_route']))
                st.info(f"Total Distance: {response_data['total_distance_km']} km")
        except requests.RequestException as e:
            st.error(f"Failed to connect to API. {str(e)}")

