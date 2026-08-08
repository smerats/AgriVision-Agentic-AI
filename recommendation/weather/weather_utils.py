"""Small, reusable weather checks used by the recommendation module."""

import math
from typing import Any, Iterable, Optional


def to_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """Convert a weather value to a number without masking missing data."""
    try:
        converted = float(value)
    except (TypeError, ValueError):
        return default
    return converted if math.isfinite(converted) else default


def is_heavy_rain(rainfall_mm: Any, threshold_mm: float = 25.0) -> bool:
    """Return whether rainfall meets the heavy-rain threshold."""
    value = to_float(rainfall_mm)
    return value is not None and value >= threshold_mm


def has_insufficient_rainfall(rainfall_mm: Any, threshold_mm: float = 5.0) -> bool:
    """Return whether rainfall is too low to meaningfully wet a field."""
    value = to_float(rainfall_mm)
    return value is not None and value < threshold_mm


def is_high_temperature(temperature_c: Any, threshold_c: float = 35.0) -> bool:
    """Return whether temperature is high enough to create heat stress."""
    value = to_float(temperature_c)
    return value is not None and value >= threshold_c


def is_low_temperature(temperature_c: Any, threshold_c: float = 10.0) -> bool:
    """Return whether temperature is low enough to slow crop growth."""
    value = to_float(temperature_c)
    return value is not None and value <= threshold_c


def is_high_humidity(humidity_percent: Any, threshold_percent: float = 80.0) -> bool:
    """Return whether humidity is high enough to increase disease pressure."""
    value = to_float(humidity_percent)
    return value is not None and value >= threshold_percent


def is_strong_wind(wind_speed_mps: Any, threshold_mps: float = 10.0) -> bool:
    """Return whether wind speed is high enough to disrupt field work."""
    value = to_float(wind_speed_mps)
    return value is not None and value >= threshold_mps


def classify_weather_risk(
    temperature_c: Any,
    rainfall_mm: Any,
    humidity_percent: Any,
    wind_speed_mps: Any,
) -> dict:
    """Classify overall weather risk and return the contributing conditions."""
    conditions = []
    if is_heavy_rain(rainfall_mm):
        conditions.append("heavy_rain")
    if has_insufficient_rainfall(rainfall_mm):
        conditions.append("insufficient_rainfall")
    if is_high_temperature(temperature_c):
        conditions.append("high_temperature")
    if is_low_temperature(temperature_c):
        conditions.append("low_temperature")
    if is_high_humidity(humidity_percent):
        conditions.append("high_humidity")
    if is_strong_wind(wind_speed_mps):
        conditions.append("strong_wind")

    if len(conditions) >= 2 or any(
        condition in conditions for condition in ("heavy_rain", "high_temperature", "strong_wind")
    ):
        level = "high"
    elif conditions:
        level = "moderate"
    else:
        level = "low"

    return {"level": level, "conditions": conditions}


def first_number(values: Iterable[Any], default: float = 0.0) -> float:
    """Return the first value that can be converted to a float."""
    for value in values:
        try:
            converted = to_float(value)
            if converted is not None:
                return converted
        except (TypeError, ValueError):
            continue
    return default
