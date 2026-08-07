"""
disease_prediction/train.py
Trains a RandomForestClassifier model for Disease risk prediction.
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
        print("Generating synthetic Disease Prediction dataset...")
        n_samples = 500
        
        humidity = np.random.uniform(40.0, 95.0, n_samples)          # %
        temperature = np.random.uniform(15.0, 35.0, n_samples)       # °C
        rainfall = np.random.uniform(0.0, 150.0, n_samples)          # mm
        leaf_wetness = np.random.uniform(0.0, 18.0, n_samples)       # hours/day
        
        # Calculate risk scores (humidity and leaf wetness are primary disease drivers)
        risk_score = (
            0.03 * humidity 
            + 0.05 * leaf_wetness 
            + 0.01 * rainfall 
            - 0.01 * (temperature - 26)**2
            - 3.5  # shift intercept
        )
        prob = 1.0 / (1.0 + np.exp(-risk_score))
        disease_risk = (np.random.rand(n_samples) < prob).astype(int)
        
        df = pd.DataFrame({
            "humidity": humidity,
            "temperature": temperature,
            "rainfall": rainfall,
            "leaf_wetness": leaf_wetness,
            "disease_risk": disease_risk
        })
        df.to_csv(dataset_path, index=False)
        print(f"Dataset saved to {dataset_path}")
    else:
        print("Loading existing Disease Prediction dataset...")
        df = pd.read_csv(dataset_path)

    # 2. Train the model
    feature_cols = ["humidity", "temperature", "rainfall", "leaf_wetness"]
    X = df[feature_cols]
    y = df["disease_risk"]

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
        "feature_importances": feature_importances
    }

    model_pkl_path = os.path.join(model_dir, "model.pkl")
    joblib.dump(model_data, model_pkl_path)
    print(f"Model and metadata successfully saved to {model_pkl_path}")

if __name__ == "__main__":
    main()
