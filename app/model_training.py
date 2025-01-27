#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load the combined data
df = pd.read_csv("combined_delhi_delivery_data.csv")

# Define features and target
# Note: 'total_delivery_time' would need to be calculated based on base_delivery_time, traffic_delay, and weather_impact
df['total_delivery_time'] = df['distance'] * 120 + df['traffic_delay'] * 60 + (df['distance'] * df['weather_impact'] / 10)
X = df.drop(columns=["order_id", "total_delivery_time"])
y = df["total_delivery_time"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Use GridSearchCV for better tuning of Random Forest
rf_params = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}
rf = RandomForestRegressor(random_state=42)
grid_rf = GridSearchCV(rf, rf_params, cv=5, n_jobs=-1, verbose=1)
grid_rf.fit(X_train, y_train)

# Train the best model found
best_rf = grid_rf.best_estimator_
best_rf.fit(X_train, y_train)

# Predict and evaluate
y_pred = best_rf.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f} seconds")

# Save the best model
joblib.dump(best_rf, "delhi_delivery_time_model.pkl")
print("Best model for Delhi saved as 'delhi_delivery_time_model.pkl'.")

