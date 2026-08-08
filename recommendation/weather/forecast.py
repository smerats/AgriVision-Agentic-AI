"""Agricultural recommendations derived from normalized weather data."""

from typing import Optional

from .weather_utils import (
    classify_weather_risk,
    has_insufficient_rainfall,
    is_heavy_rain,
    is_high_temperature,
    is_low_temperature,
    is_strong_wind,
    to_float,
)


def _value(data: dict, key: str) -> Optional[float]:
    return to_float(data.get(key))


def _forecast_summary(forecast: list[dict]) -> dict:
    """Summarize forecast hazards without coupling the rules to an API format."""
    rainfall = [value for value in (_value(item, "rainfall_mm") for item in forecast) if value is not None]
    temperatures = [value for value in (_value(item, "temperature_c") for item in forecast) if value is not None]
    wind = [value for value in (_value(item, "wind_speed_mps") for item in forecast) if value is not None]
    return {
        "heavy_rain_expected": any(is_heavy_rain(value) for value in rainfall),
        "insufficient_rain_expected": bool(rainfall) and all(
            has_insufficient_rainfall(value) for value in rainfall
        ),
        "high_temperature_expected": any(is_high_temperature(value) for value in temperatures),
        "low_temperature_expected": any(is_low_temperature(value) for value in temperatures),
        "strong_wind_expected": any(is_strong_wind(value) for value in wind),
    }


def _recommendation_output(weather_status: str, risk: str, recommendations: list[str]) -> dict:
    """Build the stable public output contract for this module."""
    return {
        "weather_status": weather_status,
        "risk": risk,
        "recommendations": recommendations,
    }


def _weather_status(
    rainfall: float,
    temperature: float,
    wind_speed: float,
    forecast_risks: dict,
) -> str:
    """Choose the dominant condition for the public recommendation output."""
    rain_expected = is_heavy_rain(rainfall) or forecast_risks["heavy_rain_expected"]
    high_temperature = is_high_temperature(temperature) or forecast_risks["high_temperature_expected"]
    low_temperature = is_low_temperature(temperature) or forecast_risks["low_temperature_expected"]
    dry = has_insufficient_rainfall(rainfall) or forecast_risks["insufficient_rain_expected"]

    if rain_expected:
        return "rain_expected"
    if high_temperature and dry:
        return "hot_and_dry"
    if high_temperature:
        return "high_temperature"
    if low_temperature:
        return "low_temperature"
    if is_strong_wind(wind_speed) or forecast_risks["strong_wind_expected"]:
        return "strong_wind"
    if dry or has_insufficient_rainfall(rainfall):
        return "dry"
    return "normal"


def _risk_level(current_risk: dict, forecast_risks: dict) -> str:
    """Elevate current risk when upcoming weather adds a significant hazard."""
    if current_risk["level"] == "high":
        return "high"
    if any(
        forecast_risks[key]
        for key in ("heavy_rain_expected", "high_temperature_expected", "strong_wind_expected")
    ):
        return "high"
    if current_risk["level"] == "moderate" or forecast_risks["low_temperature_expected"] or forecast_risks[
        "insufficient_rain_expected"
    ]:
        return "moderate"
    return "low"


def generate_recommendations(weather_data: dict) -> dict:
    """Generate an exact three-field agricultural recommendation object."""
    if not isinstance(weather_data, dict):
        return _recommendation_output(
            "unknown", "high", ["Weather data is unavailable; postpone weather-sensitive field work."]
        )

    current = weather_data.get("current", weather_data)
    if not isinstance(current, dict):
        return _recommendation_output(
            "unknown", "high", ["Current weather data is unavailable; postpone weather-sensitive field work."]
        )

    required_fields = ("temperature_c", "rainfall_mm", "humidity_percent", "wind_speed_mps")
    missing_fields = [field for field in required_fields if to_float(current.get(field)) is None]
    if missing_fields:
        return _recommendation_output(
            "unknown",
            "high",
            [
                "Weather data is incomplete; postpone weather-sensitive field work until conditions are confirmed.",
            ],
        )

    temperature = _value(current, "temperature_c")
    rainfall = _value(current, "rainfall_mm")
    humidity = _value(current, "humidity_percent")
    wind_speed = _value(current, "wind_speed_mps")
    current_risk = classify_weather_risk(temperature, rainfall, humidity, wind_speed)
    forecast = weather_data.get("forecast", [])
    if not isinstance(forecast, list):
        forecast = []
    forecast_risks = _forecast_summary([item for item in forecast if isinstance(item, dict)])
    rain_expected = is_heavy_rain(rainfall) or forecast_risks["heavy_rain_expected"]
    dry_expected = has_insufficient_rainfall(rainfall) or forecast_risks["insufficient_rain_expected"]
    recommendations = []

    if rain_expected:
        recommendations.extend(
            [
                "Avoid irrigation today.",
                "Delay fertilizer application until rainfall decreases.",
                "Monitor the field for waterlogging.",
            ]
        )
    elif dry_expected:
        recommendations.extend(
            [
                "Check soil moisture and irrigate according to crop needs.",
                "Apply fertilizer only when the soil is adequately moist.",
            ]
        )
    elif has_insufficient_rainfall(rainfall):
        recommendations.append("Check soil moisture before deciding whether to irrigate.")
    else:
        recommendations.append("Monitor soil moisture and avoid unnecessary irrigation.")

    if not rain_expected:
        recommendations.append("Apply fertilizer only when the soil is workable and weather remains suitable.")

    activity_reasons = []
    if is_high_temperature(temperature) or forecast_risks["high_temperature_expected"]:
        activity_reasons.append("high temperatures")
    if is_low_temperature(temperature) or forecast_risks["low_temperature_expected"]:
        activity_reasons.append("low temperatures")
    if is_strong_wind(wind_speed) or forecast_risks["strong_wind_expected"]:
        activity_reasons.append("strong winds")
    if activity_reasons:
        recommendations.append(
            f"Postpone spraying, transplanting and exposed field work during {', '.join(activity_reasons)}."
        )
    elif rain_expected:
        recommendations.append(
            "Clear drainage channels and keep machinery off saturated fields until the soil firms up."
        )
    elif humidity >= 80:
        recommendations.append(
            "Inspect leaves for fungal symptoms and avoid working wet foliage while humidity remains high."
        )
    else:
        recommendations.append("Use the dry, calm conditions to scout crops and remove weeds.")

    if humidity >= 80:
        recommendations.append("Monitor crops closely for moisture-related disease pressure in the humid conditions.")

    return _recommendation_output(
        _weather_status(rainfall, temperature, wind_speed, forecast_risks),
        _risk_level(current_risk, forecast_risks),
        recommendations,
    )


# Short alias for integrations that prefer an action-oriented function name.
recommend_weather = generate_recommendations
