"""
pest_prediction/train.py
Trains a RandomForestClassifier model for Pest risk prediction.
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
        print("Generating synthetic Pest Prediction dataset...")
        n_samples = 500
        
        temperature = np.random.uniform(15.0, 35.0, n_samples)       # °C
        humidity = np.random.uniform(40.0, 95.0, n_samples)          # %
        rainfall = np.random.uniform(0.0, 150.0, n_samples)          # mm
        crop_density = np.random.uniform(1.0, 10.0, n_samples)       # plants / sq. meter
        
        # Risk score calculation (high temperature, high humidity, high crop density favor pests)
        risk_score = (
            0.1 * temperature
            + 0.05 * humidity
            + 0.2 * crop_density
            - 0.01 * rainfall
            - 8.0 # shift intercept
        )
        
        # Classify risk score into 3 categories (0: Low, 1: Medium, 2: High)
        pest_risk = np.zeros(n_samples, dtype=int)
        pest_risk[risk_score > -1.0] = 1
        pest_risk[risk_score > 1.5] = 2
        
        df = pd.DataFrame({
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "crop_density": crop_density,
            "pest_risk": pest_risk
        })
        df.to_csv(dataset_path, index=False)
        print(f"Dataset saved to {dataset_path}")
    else:
        print("Loading existing Pest Prediction dataset...")
        df = pd.read_csv(dataset_path)

    # 2. Train the model
    feature_cols = ["temperature", "humidity", "rainfall", "crop_density"]
    X = df[feature_cols]
    y = df["pest_risk"]

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
        "target_mapping": {0: "Low", 1: "Medium", 2: "High"}
    }

    model_pkl_path = os.path.join(model_dir, "model.pkl")
    joblib.dump(model_data, model_pkl_path)
    print(f"Model and metadata successfully saved to {model_pkl_path}")

if __name__ == "__main__":
    main()
