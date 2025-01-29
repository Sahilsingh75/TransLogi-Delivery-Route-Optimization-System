# TransLogi Delivery Route Optimization System

Welcome to the TransLogi Delivery Route Optimization System, a comprehensive project designed to enhance logistics operations for TransLogi, a fictional logistics company. This system integrates predictive analytics, route optimization, and real-time monitoring to streamline delivery processes.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Additional Setup for the Model](#additional-setup-for-the-model)
- [Usage](#usage)
- [Components](#components)
- [Future Enhancements](#future-enhancements)

## Overview

This system is designed to:
- Predict delivery times for new orders.
- Optimize delivery routes for multiple vehicles considering traffic, weather, and order constraints.
- Provide a web-based dashboard for real-time monitoring using Streamlit.

## Project Structure
  ```
  translogi_delivery_optimization/
  ├── app/
  │   ├── data_collection.py        # Simulates and collects data
  │   ├── gui.py                    # Streamlit web interface
  │   ├── main.py                   # FastAPI backend
  │   └── model_training.py         # Machine learning model training
  ├── data/                         # Contains datasets
  │   ├── combined_delhi_delivery_data.csv
  │   ├── delhi_places.csv
  │   ├── simulated_delivery_data.csv
  │   ├── simulated_traffic_data.csv
  │   └── simulated_weather_data.csv
  ├── img/                          # Contains images/screenshots
  │   ├── gui_screenshot1.png
  │   └── gui_screenshot2.png
  ├── model/                        # Pre-trained model files
  │   └── delhi_delivery_time_model.pkl (Model needs to be downloaded separately)
  ├── notebooks/                    # Jupyter Notebooks for development
  │   ├── data_collection.ipynb
  │   ├── gui.ipynb
  │   ├── main.ipynb
  │   └── model_training.ipynb
  ├── requirements.txt              # Python dependencies
  └── README.md                     # Project documentation
  ```

## Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Streamlit (for the web-based UI)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Sahilsingh75/TransLogi-Delivery-Route-Optimization-System.git
   cd translogi_delivery_optimization
   ```
2. **Create a Virtual Environment (Optional but Recommended)**:
   ```bash
   python -m venv venv
   ```
   Activate it:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`
   
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Note: You need to replace `your_google_maps_api_key` and `your_openweather_api_key` with your actual API keys in `app/main.py`.

### Additional Setup for the Model
Before running the application, you must download the delivery time prediction model due to its large size. Please refer to the `model_download_instructions.txt` file in the repository for detailed instructions on how to obtain and integrate the model with the system.

## Usage

### Running the Backend (FastAPI)
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
This command starts the server on `http://127.0.0.1:8000`. Access the API documentation via Swagger UI at `http://127.0.0.1:8000/docs`.

### Running the Web Interface (Streamlit GUI)
Launch the Streamlit web app:
```bash
streamlit run app/gui.py
```
This will open a browser window where you can interact with the system's functionalities.

## API Endpoints

### Predict Delivery Time
Send a POST request to `/predict_delivery_time/` with JSON payload like:
```json
{
  "pickup_location": "Connaught Place",
  "delivery_location": "India Gate",
  "order_weight": 5.0
}
```
This endpoint returns the predicted delivery time along with other details like distance, traffic duration, and weather conditions.

### Optimize Routes
Send a POST request to `/optimize_routes/` with JSON payload like:
```json
{
  "pickup_location": "Connaught Place",
  "delivery_locations": ["India Gate", "Red Fort", "Qutub Minar"]
}
```
This endpoint returns an optimized route list and the total distance.

## GUI Application (Streamlit)
The GUI provides an intuitive web-based interface:

- **Pickup and Delivery Location Selection**: Dropdowns for selecting locations from `delhi_places.csv`.
- **Order Weight Input**: Entry field for the weight of the order.
- **Predict Delivery Time Button**: Triggers the prediction API call and displays the estimated time.
- **Route Optimization**: Visualizes optimized routes on an interactive map.

## Future Enhancements
- Implement user authentication for personalized order tracking.
- Integrate live traffic data for real-time route adjustments.
- Develop a mobile-friendly version of the dashboard.
- Extend support for multiple cities beyond Delhi.

---
This project aims to provide an efficient, AI-driven logistics optimization system. Feel free to contribute, report issues, or suggest improvements!

For inquiries, contact **Sahil Singh** at [GitHub](https://github.com/Sahilsingh75).

