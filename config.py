"""
config.py
Central configuration for the AgriVision AI backend.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AI_MODELS_DIR = os.path.abspath(os.path.join(BASE_DIR, "ai-models"))


class Config:
    """Base Flask configuration."""

    DEBUG = os.environ.get("FLASK_DEBUG", "True") == "True"
    HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
    PORT = int(os.environ.get("FLASK_PORT", 5000))

    # Absolute paths to each AI model's directory. The service layer uses
    # these to dynamically load each model's independent predict.py module.
    CROP_YIELD_DIR = os.path.join(AI_MODELS_DIR, "crop_yield")
    DISEASE_DIR = os.path.join(AI_MODELS_DIR, "disease_prediction")
    PEST_DIR = os.path.join(AI_MODELS_DIR, "pest_prediction")
    CLIMATE_DIR = os.path.join(AI_MODELS_DIR, "climate_prediction")