"""
disease_prediction/predict.py
Runs predictions for Disease Prediction and integrates Explainable AI.
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
    Predict disease risk based on input data and return prediction, confidence, and explanation.
    
    Expected keys in input_data:
      - humidity
      - temperature
      - rainfall
      - leaf_wetness
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
        raise KeyError(f"Missing required disease prediction feature: {e}")
        
    import pandas as pd
    features_2d = pd.DataFrame([features_list], columns=feature_names)
    model = model_data["model"]
    
    # Predict risk class
    prediction_class = int(model.predict(features_2d)[0])
    probabilities = model.predict_proba(features_2d)[0]
    
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
        target_name="Disease Risk"
    )
    
    return {
        "status": "success",
        "disease_prediction": "High Risk" if prediction_class == 1 else "Low Risk",
        "disease_probability": float(probabilities[1]),
        "confidence": confidence,
        "explanation": explanation
    }
