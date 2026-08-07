"""
controllers/prediction_controller.py
Handles HTTP request parsing/validation and response formatting.
All actual AI/ML work is delegated to the service layer, keeping this
layer thin and focused on the HTTP contract.
"""

from flask import request, jsonify

from services.prediction_service import PredictionService
from utils.helper import validate_payload, error_response

service = PredictionService()


def health_check():
    return jsonify(
        {
            "status": "ok",
            "service": "AgriVision AI Backend",
            "message": "Service is running",
        }
    ), 200


def predict_crop_yield():
    data = request.get_json(silent=True)
    valid, msg = validate_payload(
        data, required_fields=["rainfall", "temperature", "soil_ph", "humidity", "fertilizer_usage"]
    )
    if not valid:
        return error_response(msg)
    try:
        result = service.get_crop_yield_prediction(data)
        return jsonify(result), 200
    except Exception as exc:  # noqa: BLE001 - surface a clean error to the client
        return error_response(f"Prediction failed: {exc}", status_code=500)


def predict_disease():
    data = request.get_json(silent=True)
    valid, msg = validate_payload(
        data, required_fields=["humidity", "temperature", "rainfall", "leaf_wetness"]
    )
    if not valid:
        return error_response(msg)
    try:
        result = service.get_disease_prediction(data)
        return jsonify(result), 200
    except Exception as exc:  # noqa: BLE001
        return error_response(f"Prediction failed: {exc}", status_code=500)


def predict_pest():
    data = request.get_json(silent=True)
    valid, msg = validate_payload(
        data, required_fields=["temperature", "humidity", "rainfall", "crop_density"]
    )
    if not valid:
        return error_response(msg)
    try:
        result = service.get_pest_prediction(data)
        return jsonify(result), 200
    except Exception as exc:  # noqa: BLE001
        return error_response(f"Prediction failed: {exc}", status_code=500)


def predict_climate():
    data = request.get_json(silent=True)
    valid, msg = validate_payload(
        data, required_fields=["temperature", "rainfall", "humidity", "wind_speed"]
    )
    if not valid:
        return error_response(msg)
    try:
        result = service.get_climate_prediction(data)
        return jsonify(result), 200
    except Exception as exc:  # noqa: BLE001
        return error_response(f"Prediction failed: {exc}", status_code=500)