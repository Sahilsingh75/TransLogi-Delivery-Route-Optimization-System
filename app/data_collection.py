#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import numpy as np
from scipy.stats import norm
import random

# Define New Delhi's geographical boundaries
LAT_NORTH, LAT_SOUTH = 28.7041, 28.5135
LON_EAST, LON_WEST = 77.3072, 77.0266

def generate_delivery_data(n=10000):
    delivery_data = []
    
    for i in range(1, n + 1):
        customer_lat = round(random.uniform(LAT_SOUTH, LAT_NORTH), 6)
        customer_lon = round(random.uniform(LON_WEST, LON_EAST), 6)
        
        distance = norm.rvs(loc=5, scale=2, size=1)[0]  # Average distance with variation
        distance = round(max(1, distance), 2)  # Minimum 1 km
        order_weight = round(np.random.uniform(0.5, 10), 2)  # Weight in kg
        
        delivery_data.append({
            "order_id": i,
            "customer_lat": customer_lat,
            "customer_lon": customer_lon,
            "distance": distance,
            "order_weight": order_weight
        })
    
    return pd.DataFrame(delivery_data)

# Generate and save delivery data
delivery_df = generate_delivery_data()
delivery_df.to_csv("simulated_delivery_data.csv", index=False)
print("Delivery data generated and saved.")

def generate_traffic_data(n=10000):
    traffic_data = []
    
    for i in range(1, n + 1):
        time_of_day = np.random.choice(['Morning', 'Afternoon', 'Evening'], p=[0.3, 0.4, 0.3])
        if time_of_day == 'Morning':
            traffic_condition = np.random.choice(['Low', 'Medium', 'High'], p=[0.5, 0.3, 0.2])
            traffic_delay = {'Low': 5, 'Medium': 10, 'High': 15}[traffic_condition]
        elif time_of_day == 'Evening':
            traffic_condition = np.random.choice(['Low', 'Medium', 'High'], p=[0.2, 0.4, 0.4])
            traffic_delay = {'Low': 10, 'Medium': 20, 'High': 30}[traffic_condition]
        else:  # Afternoon
            traffic_condition = np.random.choice(['Low', 'Medium'], p=[0.7, 0.3])
            traffic_delay = {'Low': 5, 'Medium': 10}[traffic_condition]
        
        traffic_data.append({
            "order_id": i,
            "time_of_day": time_of_day,
            "traffic_condition": traffic_condition,
            "traffic_delay": traffic_delay
        })
    
    return pd.DataFrame(traffic_data)

# Generate and save traffic data
traffic_df = generate_traffic_data()
traffic_df.to_csv("simulated_traffic_data.csv", index=False)
print("Traffic data generated and saved.")


def generate_weather_data(n=10000):
    weather_data = []
    
    for i in range(1, n + 1):
        weather_conditions = ['Clear', 'Rainy', 'Foggy', 'Hazy']
        weather_condition = np.random.choice(weather_conditions, p=[0.5, 0.25, 0.15, 0.1])
        temperature = np.random.randint(5, 45)  # Temperature in Celsius, Delhi's range
        weather_impact = {
            'Clear': 0,
            'Rainy': 15,
            'Foggy': 20,
            'Hazy': 5
        }[weather_condition]
        
        weather_data.append({
            "order_id": i,
            "weather_condition": weather_condition,
            "temperature": temperature,
            "weather_impact": weather_impact
        })
    
    return pd.DataFrame(weather_data)

# Generate and save weather data
weather_df = generate_weather_data()
weather_df.to_csv("simulated_weather_data.csv", index=False)
print("Weather data generated and saved.")



# In[13]:


# Load datasets
delivery_df = pd.read_csv("simulated_delivery_data.csv")
traffic_df = pd.read_csv("simulated_traffic_data.csv")
weather_df = pd.read_csv("simulated_weather_data.csv")

# Merge datasets
merged_df = delivery_df.merge(traffic_df, on="order_id").merge(weather_df, on="order_id")

# Feature Engineering
merged_df = pd.get_dummies(merged_df, columns=['time_of_day', 'traffic_condition', 'weather_condition'])

# Save combined dataset
merged_df.to_csv("combined_delhi_delivery_data.csv", index=False)
print("Combined dataset saved for model training.")

