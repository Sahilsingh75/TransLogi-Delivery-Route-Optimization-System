#!/usr/bin/env python
# coding: utf-8

# In[7]:


from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import googlemaps
import requests
import joblib
import os
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import logging
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Load the trained model
try:
    model = joblib.load("delivery_time_model.pkl")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    model = None

# API Keys
GOOGLE_MAPS_API_KEY = "use your api key"
OPENWEATHER_API_KEY = "use your api key"

# Initialize Google Maps Client
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Request body models
class DeliveryRequest(BaseModel):
    pickup_location: str
    delivery_location: str
    order_weight: float

class RouteOptimizationRequest(BaseModel):
    pickup_location: str
    delivery_locations: List[str]  # List of delivery locations as strings

# API endpoint to predict delivery time
@app.post("/predict_delivery_time/")
async def predict_delivery_time(request: DeliveryRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Step 1: Get distance and duration from Google Maps API
    try:
        directions_result = gmaps.directions(
            origin=request.pickup_location,
            destination=request.delivery_location,
            mode="driving",
            traffic_model="best_guess",
            departure_time="now"
        )
        if not directions_result:
            raise HTTPException(status_code=400, detail="Could not fetch route details from Google Maps.")
        
        distance = directions_result[0]['legs'][0]['distance']['value'] / 1000  # in km
        traffic_duration = directions_result[0]['legs'][0]['duration_in_traffic']['value'] / 60  # in minutes

        # Step 2: Get weather data from OpenWeather API
        location_coords = directions_result[0]['legs'][0]['start_location']
        latitude, longitude = location_coords['lat'], location_coords['lng']
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPENWEATHER_API_KEY}&units=metric"
        weather_response = requests.get(weather_url).json()

        if weather_response.get("cod") != 200:
            raise HTTPException(status_code=400, detail="Could not fetch weather details.")

        weather_main = weather_response['weather'][0]['main']
        temperature = weather_response['main']['temp']
        weather_impact = 10 if weather_main in ["Rain", "Snow", "Thunderstorm"] else 5  # Example weight

        # Step 3: Prepare features for prediction
        features = [[
            distance,
            request.order_weight,
            traffic_duration,
            weather_impact,
            temperature
        ]]

        # Step 4: Predict delivery time
        predicted_time = model.predict(features)
        return {
            "predicted_delivery_time": round(predicted_time[0], 2),
            "distance_km": distance,
            "traffic_duration_min": traffic_duration,
            "temperature_c": temperature,
            "weather_condition": weather_main
        }
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize_routes/")
async def optimize_routes(request: RouteOptimizationRequest):
    # Step 1: Get distance matrix using Google Maps Distance Matrix API
    try:
        all_locations = [request.pickup_location] + request.delivery_locations
        distance_matrix = gmaps.distance_matrix(
            origins=all_locations,
            destinations=all_locations,
            mode="driving",
            traffic_model="best_guess",
            departure_time="now"
        )
        
        # Extract distances in meters and convert to km
        distances = [
            [element['distance']['value'] / 1000 for element in row['elements']]
            for row in distance_matrix['rows']
        ]
        
        # Step 2: Set up OR-Tools routing solver
        manager = pywrapcp.RoutingIndexManager(len(distances), 1, 0)  # Single vehicle, depot at index 0
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Callback to return distances between nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(distances[from_node][to_node] * 1000)  # Convert back to meters

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Step 3: Solve the problem
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            # Extract optimized route
            index = routing.Start(0)
            route = []
            total_distance = 0
            while not routing.IsEnd(index):
                route.append(all_locations[manager.IndexToNode(index)])
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

            route.append(all_locations[0])  # Return to depot
            total_distance /= 1000  # Convert meters to km
            return {
                "optimized_route": route,
                "total_distance_km": total_distance
            }
        else:
            raise HTTPException(status_code=400, detail="Could not solve the route optimization problem.")
    except Exception as e:
        logging.error(f"Error in route optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Configure logging
logging.basicConfig(
    filename="api_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logging.info(f"Response Status: {response.status_code}")
        return response
    except Exception as e:
        logging.error(f"Error: {e}")
        raise

