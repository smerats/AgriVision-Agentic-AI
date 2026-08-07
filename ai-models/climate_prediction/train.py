"""
climate_prediction/train.py
Trains a RandomForestClassifier model for Climate prediction.
Generates a synthetic dataset.csv if it does not exist.
"""

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

def main():
    # Set seed for reproducibility
    np.random.seed(42)

    # Directory setup
    model_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(model_dir, "dataset.csv")

    # 1. Generate synthetic dataset if it doesn't exist
    if not os.path.exists(dataset_path):
        print("Generating synthetic Climate dataset...")
        n_samples = 500
        
        temperature = np.random.uniform(10.0, 40.0, n_samples)       # °C
        rainfall = np.random.uniform(0.0, 200.0, n_samples)          # mm
        humidity = np.random.uniform(30.0, 95.0, n_samples)          # %
        wind_speed = np.random.uniform(0.0, 60.0, n_samples)         # km/h
        
        # Assign condition classes (0: Sunny, 1: Rainy, 2: Stormy)
        climate_condition = np.zeros(n_samples, dtype=int)
        
        for i in range(n_samples):
            if rainfall[i] > 100.0 and wind_speed[i] > 35.0:
                climate_condition[i] = 2  # Stormy
            elif rainfall[i] > 30.0 or humidity[i] > 75.0:
                climate_condition[i] = 1  # Rainy
            else:
                climate_condition[i] = 0  # Sunny
        
        df = pd.DataFrame({
            "temperature": temperature,
            "rainfall": rainfall,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "climate_condition": climate_condition
        })
        df.to_csv(dataset_path, index=False)
        print(f"Dataset saved to {dataset_path}")
    else:
        print("Loading existing Climate dataset...")
        df = pd.read_csv(dataset_path)

    # 2. Train the model
    feature_cols = ["temperature", "rainfall", "humidity", "wind_speed"]
    X = df[feature_cols]
    y = df["climate_condition"]

    print("Training RandomForestClassifier model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # 3. Compute statistics for explainability
    feature_means = X.mean().to_dict()
    feature_importances = dict(zip(X.columns, model.feature_importances_))

    # 4. Save model and metadata
    model_data = {
        "model": model,
        "feature_names": feature_cols,
        "feature_means": feature_means,
        "feature_importances": feature_importances,
        "target_mapping": {0: "Sunny", 1: "Rainy", 2: "Stormy"}
    }

    model_pkl_path = os.path.join(model_dir, "model.pkl")
    joblib.dump(model_data, model_pkl_path)
    print(f"Model and metadata successfully saved to {model_pkl_path}")

if __name__ == "__main__":
    main()
