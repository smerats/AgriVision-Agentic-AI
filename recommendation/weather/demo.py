"""Standalone mock-data demo for the weather recommendation module."""

import json

from .forecast import generate_recommendations


MOCK_WEATHER_DATA = {
    "current": {
        "temperature_c": 24,
        "rainfall_mm": 30,
        "humidity_percent": 85,
        "wind_speed_mps": 4,
    },
    "forecast": [
        {
            "temperature_c": 23,
            "rainfall_mm": 18,
            "humidity_percent": 82,
            "wind_speed_mps": 5,
        },
        {
            "temperature_c": 25,
            "rainfall_mm": 8,
            "humidity_percent": 78,
            "wind_speed_mps": 4,
        },
    ],
}


if __name__ == "__main__":
    recommendation = generate_recommendations(MOCK_WEATHER_DATA)
    print(json.dumps(recommendation, indent=2))
