"""
pest_prediction/predict.py
Runs predictions for Pest Prediction and integrates Explainable AI.
"""

import os
import sys
import numpy as np
import joblib

# Add the parent directory of this module to sys.path so we can import explainable_ai
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from explainable_ai.confidence import get_prediction_confidence
from explainable_ai.explanation import explain_prediction

model_pkl_path = os.path.join(current_dir, "model.pkl")

# Cached model data
model_data = None

def predict(input_data: dict) -> dict:
    """
    Predict pest risk based on input data and return prediction, confidence, and explanation.
    
    Expected keys in input_data:
      - temperature
      - humidity
      - rainfall
      - crop_density
    """
    global model_data
    if model_data is None:
        if os.path.exists(model_pkl_path):
            model_data = joblib.load(model_pkl_path)
        else:
            raise FileNotFoundError("Model file model.pkl not found. Please run train.py first.")
            
    feature_names = model_data["feature_names"]
    
    try:
        features_list = [float(input_data[name]) for name in feature_names]
    except KeyError as e:
        raise KeyError(f"Missing required pest prediction feature: {e}")
        
    import pandas as pd
    features_2d = pd.DataFrame([features_list], columns=feature_names)
    model = model_data["model"]
    
    # Predict risk class
    prediction_class = int(model.predict(features_2d)[0])
    risk_label = model_data["target_mapping"].get(prediction_class, "Unknown")
    
    # Compute confidence score
    confidence = get_prediction_confidence(
        model,
        features_2d,
        target_type="classification"
    )
    
    # Compute explanations
    explanation = explain_prediction(
        feature_dict={name: float(input_data[name]) for name in feature_names},
        feature_means=model_data["feature_means"],
        feature_importances=model_data["feature_importances"],
        target_type="classification",
        target_name="Pest Risk"
    )
    
    return {
        "status": "success",
        "pest_prediction": risk_label,
        "confidence": confidence,
        "explanation": explanation
    }
