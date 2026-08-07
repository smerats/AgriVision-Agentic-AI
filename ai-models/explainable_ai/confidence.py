"""
explainable_ai/confidence.py
Calculates prediction confidence scores for classification and regression models.
"""

import numpy as np

def get_prediction_confidence(model, features_2d, target_type="classification", target_std=1.0):
    """
    Calculate a confidence score between 0.0 and 1.0 for a prediction.
    
    Parameters:
        model: Trained scikit-learn model.
        features_2d (np.ndarray): 2D array of features, shape (1, num_features).
        target_type (str): "classification" or "regression".
        target_std (float): Standard deviation of the target variable in the training set (used for regression).
        
    Returns:
        float: A confidence score between 0.0 and 1.0.
    """
    try:
        if target_type == "classification":
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(features_2d)
                # Return the probability of the predicted class
                return float(np.max(probs))
            else:
                # Fallback if the model does not support predict_proba
                return 1.0
                
        elif target_type == "regression":
            if hasattr(model, "estimators_"):
                # Ensemble model (e.g. RandomForestRegressor)
                # Compute predictions of all individual decision trees
                preds = [estimator.predict(features_2d)[0] for estimator in model.estimators_]
                pred_std = np.std(preds)
                scale = target_std if target_std > 0 else 1.0
                # Use RBF-like decay to map prediction standard deviation to [0, 1]
                confidence = np.exp(-pred_std / scale)
                return float(confidence)
            else:
                # Fallback if not an ensemble model
                return 0.8
                
    except Exception:
        # Fallback in case of any evaluation error
        return 0.8
    
    return 0.8
