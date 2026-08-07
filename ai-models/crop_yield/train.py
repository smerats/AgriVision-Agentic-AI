"""
crop_yield/train.py
Trains a RandomForestRegressor model for Crop Yield prediction.
Generates a synthetic dataset.csv if it does not exist.
"""

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

def main():
    # Set seed for reproducibility
    np.random.seed(42)

    # Directory setup
    model_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(model_dir, "dataset.csv")

    # 1. Generate synthetic dataset if it doesn't exist
    if not os.path.exists(dataset_path):
        print("Generating synthetic Crop Yield dataset...")
        n_samples = 500
        
        rainfall = np.random.uniform(50.0, 250.0, n_samples)          # mm
        temperature = np.random.uniform(15.0, 35.0, n_samples)       # °C
        soil_ph = np.random.uniform(5.5, 7.5, n_samples)              # pH
        humidity = np.random.uniform(40.0, 90.0, n_samples)            # %
        fertilizer_usage = np.random.uniform(50.0, 200.0, n_samples)  # kg/ha
        
        # Crop yield calculation with some realistic agricultural factors
        yield_val = (
            0.02 * rainfall 
            + 0.05 * fertilizer_usage 
            - 0.01 * (temperature - 25)**2 
            - 0.5 * (soil_ph - 6.5)**2
            + 0.01 * humidity
            + np.random.normal(0.0, 0.5, n_samples)
        )
        # Ensure yield is positive
        yield_val = np.maximum(0.5, yield_val)
        
        df = pd.DataFrame({
            "rainfall": rainfall,
            "temperature": temperature,
            "soil_ph": soil_ph,
            "humidity": humidity,
            "fertilizer_usage": fertilizer_usage,
            "yield": yield_val
        })
        df.to_csv(dataset_path, index=False)
        print(f"Dataset saved to {dataset_path}")
    else:
        print("Loading existing Crop Yield dataset...")
        df = pd.read_csv(dataset_path)

    # 2. Train the model
    feature_cols = ["rainfall", "temperature", "soil_ph", "humidity", "fertilizer_usage"]
    X = df[feature_cols]
    y = df["yield"]

    print("Training RandomForestRegressor model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # 3. Compute statistics for explainability
    feature_means = X.mean().to_dict()
    feature_importances = dict(zip(X.columns, model.feature_importances_))
    target_std = float(y.std())

    # 4. Save model and metadata
    model_data = {
        "model": model,
        "feature_names": feature_cols,
        "feature_means": feature_means,
        "feature_importances": feature_importances,
        "target_std": target_std
    }

    model_pkl_path = os.path.join(model_dir, "model.pkl")
    joblib.dump(model_data, model_pkl_path)
    print(f"Model and metadata successfully saved to {model_pkl_path}")

if __name__ == "__main__":
    main()
