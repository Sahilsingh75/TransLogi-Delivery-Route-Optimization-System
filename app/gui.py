#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().system('pip install streamlit')


# In[4]:


import streamlit as st
import pandas as pd
import requests

# Load Delhi places from CSV
delhi_places = pd.read_csv("delhi_places.csv")

# Helper function to get latitude and longitude
def get_coordinates(place_name):
    place = delhi_places[delhi_places['Place Name'] == place_name]
    if not place.empty:
        return place.iloc[0]['Latitude'], place.iloc[0]['Longitude']
    return None, None

# Streamlit UI setup
st.title("Delivery Time Prediction and Route Optimization")

# Dropdowns for pickup and delivery locations
pickup = st.selectbox("Select Pickup Location", delhi_places['Place Name'])
delivery = st.selectbox("Select Delivery Location", delhi_places['Place Name'])

# Input field for order weight
order_weight = st.number_input("Enter Order Weight (in kg)", min_value=0.1, step=0.1)

# Extract coordinates for selected locations
pickup_lat, pickup_lon = get_coordinates(pickup)
delivery_lat, delivery_lon = get_coordinates(delivery)

if st.button("Calculate Delivery Time"):
    if pickup == delivery:
        st.error("Pickup and Delivery locations cannot be the same.")
    else:
        # Fetch distance and traffic duration from Google Maps API
        google_maps_api_key = "AIzaSyDZSef6qd5iAIrL-vEZwKMiVm79-f6ZxZY"
        directions_url = (
            f"https://maps.googleapis.com/maps/api/directions/json?origin={pickup_lat},{pickup_lon}"
            f"&destination={delivery_lat},{delivery_lon}&mode=driving&departure_time=now"
            f"&key={google_maps_api_key}"
        )
        directions_response = requests.get(directions_url).json()

        if directions_response['status'] == 'OK':
            leg = directions_response['routes'][0]['legs'][0]
            distance_km = leg['distance']['value'] / 1000
            traffic_duration_min = leg['duration_in_traffic']['value'] / 60

            # Fetch weather data from OpenWeather API
            openweather_api_key = "264c8849e945f6a3164acba83870b513"
            weather_url = (
                f"http://api.openweathermap.org/data/2.5/weather?lat={pickup_lat}&lon={pickup_lon}"
                f"&appid={openweather_api_key}&units=metric"
            )
            weather_response = requests.get(weather_url).json()

            if weather_response.get("cod") == 200:
                weather_condition = weather_response['weather'][0]['main']
                temperature_c = weather_response['main']['temp']

                # Call FastAPI to calculate delivery time
                fastapi_url = "http://127.0.0.1:8000/predict_delivery_time/"
                delivery_request = {
                    "pickup_location": pickup,
                    "delivery_location": delivery,
                    "order_weight": order_weight
                }

                response = requests.post(fastapi_url, json=delivery_request)

                if response.status_code == 200:
                    result = response.json()
                    st.success("Delivery Time Prediction")
                    st.write(f"**Predicted Delivery Time:** {result['predicted_delivery_time']} minutes")
                    st.write(f"**Distance:** {result['distance_km']} km")
                    st.write(f"**Traffic Duration:** {result['traffic_duration_min']} minutes")
                    st.write(f"**Weather Condition:** {result['weather_condition']}")
                    st.write(f"**Temperature:** {result['temperature_c']}°C")
                else:
                    st.error("Error in FastAPI response.")
            else:
                st.error("Could not fetch weather data.")
        else:
            st.error("Could not fetch Google Maps data.")

if st.button("Optimize Routes"):
    # Example: Optimize multiple delivery points
    delivery_points = st.multiselect("Select Additional Delivery Locations", delhi_places['Place Name'])
    all_points = [pickup] + delivery_points + [delivery]

    # Call FastAPI for route optimization
    fastapi_url = "http://127.0.0.1:8000/optimize_routes/"
    optimize_request = {
        "pickup_location": pickup,
        "delivery_locations": all_points[1:]  # Exclude the first point (pickup)
    }

    response = requests.post(fastapi_url, json=optimize_request)

    if response.status_code == 200:
        result = response.json()
        st.success("Route Optimization")
        st.write(f"**Optimized Route:** {', '.join(result['optimized_route'])}")
        st.write(f"**Total Distance:** {result['total_distance_km']} km")
    else:
        st.error("Error in FastAPI response.")

