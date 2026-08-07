"""
services/prediction_service.py
Bridges the Flask backend to the independent AI model modules under
/ai-models. Each model's predict.py is self-contained and reusable
outside of this backend -- this service just dynamically loads each
model's predict() function and calls it, keeping the backend decoupled
from any specific model's internals.
"""

import os
import sys
import importlib.util

from config import Config


def _load_predict_function(model_dir: str, unique_module_name: str):
    """
    Dynamically load a model's predict.py as a uniquely-named module and
    return its predict() function. Using a unique module name (rather than
    a plain 'predict') avoids collisions when multiple models each ship
    their own predict.py file.
    """
    file_path = os.path.join(model_dir, "predict.py")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"predict.py not found for model at {model_dir}")

    spec = importlib.util.spec_from_file_location(unique_module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[unique_module_name] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "predict"):
        raise AttributeError(f"{file_path} does not define a predict() function")

    return module.predict


class PredictionService:
    """Thin orchestration layer: one method per AI model, one call each."""

    def get_crop_yield_prediction(self, input_data: dict) -> dict:
        predict_fn = _load_predict_function(Config.CROP_YIELD_DIR, "crop_yield_predict")
        return predict_fn(input_data)

    def get_disease_prediction(self, input_data: dict) -> dict:
        predict_fn = _load_predict_function(Config.DISEASE_DIR, "disease_predict")
        return predict_fn(input_data)

    def get_pest_prediction(self, input_data: dict) -> dict:
        predict_fn = _load_predict_function(Config.PEST_DIR, "pest_predict")
        return predict_fn(input_data)

    def get_climate_prediction(self, input_data: dict) -> dict:
        predict_fn = _load_predict_function(Config.CLIMATE_DIR, "climate_predict")
        return predict_fn(input_data)
