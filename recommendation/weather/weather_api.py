"""OpenWeatherMap accessors with normalized, backend-independent results."""

import json
import os
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Optional

from .weather_utils import to_float


CURRENT_WEATHER_URL = os.environ.get(
    "WEATHER_CURRENT_API_URL", "https://api.openweathermap.org/data/2.5/weather"
)
FORECAST_URL = os.environ.get(
    "WEATHER_FORECAST_API_URL", "https://api.openweathermap.org/data/2.5/forecast"
)
API_KEY_ENVIRONMENT_VARIABLE = "OPENWEATHER_API_KEY"
DEFAULT_TIMEOUT_SECONDS = 10

RequestFunction = Callable[..., Any]


def _error(message: str, code: str = "weather_api_error") -> dict:
    return {"status": "error", "error": {"code": code, "message": message}}


def _location_parameters(
    location: Optional[str], latitude: Optional[float], longitude: Optional[float]
) -> tuple[Optional[dict], Optional[dict]]:
    """Build either a city query or a coordinate query."""
    if location and (latitude is not None or longitude is not None):
        return None, _error("Provide location or latitude/longitude, not both.", "invalid_location")
    if isinstance(location, str) and location.strip():
        return {"q": location.strip()}, None
    if location is not None and not isinstance(location, str):
        return None, _error("Location must be a non-empty string.", "invalid_location")
    if latitude is None and longitude is None:
        return None, _error("A location or both latitude and longitude are required.", "invalid_location")
    if latitude is None or longitude is None:
        return None, _error("Both latitude and longitude are required.", "invalid_coordinates")
    latitude_value = to_float(latitude)
    longitude_value = to_float(longitude)
    if latitude_value is None or longitude_value is None:
        return None, _error("Latitude and longitude must be numeric.", "invalid_coordinates")
    if not -90 <= latitude_value <= 90 or not -180 <= longitude_value <= 180:
        return None, _error("Latitude or longitude is outside its valid range.", "invalid_coordinates")
    return {"lat": latitude_value, "lon": longitude_value}, None


def _request_json(
    url: str,
    params: dict,
    timeout: int,
    request_fn: Optional[RequestFunction] = None,
) -> tuple[Optional[dict], Optional[dict]]:
    request = urllib.request.Request(
        f"{url}?{urllib.parse.urlencode(params)}",
        headers={"Accept": "application/json"},
    )
    opener = request_fn or urllib.request.urlopen
    try:
        response = opener(request, timeout=timeout)
        with response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code in (401, 403):
            return None, _error("The weather API key was rejected.", "authentication_error")
        if error.code == 404:
            return None, _error("The requested location was not found.", "location_not_found")
        return None, _error(f"Weather API request failed with HTTP {error.code}.", "http_error")
    except urllib.error.URLError as error:
        return None, _error(f"Weather API connection failed: {error.reason}.", "connection_error")
    except (TimeoutError, socket.timeout):
        return None, _error("The weather API request timed out.", "timeout")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, _error("The weather API returned invalid JSON.", "invalid_response")
    except (OSError, ValueError) as error:
        return None, _error(f"Weather API request could not be completed: {error}.", "request_error")

    if not isinstance(payload, dict):
        return None, _error("The weather API returned an unexpected response.", "invalid_response")
    if payload.get("cod") not in (None, 200, "200"):
        return None, _error(str(payload.get("message", "The weather API returned an error.")), "api_error")
    return payload, None


def _api_key(api_key: Optional[str]) -> Optional[str]:
    configured_key = api_key or os.environ.get(API_KEY_ENVIRONMENT_VARIABLE) or os.environ.get(
        "WEATHER_API_KEY"
    )
    return configured_key.strip() if isinstance(configured_key, str) and configured_key.strip() else None


def _base_params(api_key: Optional[str], units: str) -> dict:
    return {"appid": api_key, "units": units}


def _mapping(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _rainfall(payload: dict, period: str = "1h") -> float:
    rain = _mapping(payload.get("rain"))
    return to_float(rain.get(period), to_float(rain.get("3h"), 0.0)) or 0.0


def _normalize_current(payload: dict) -> dict:
    main = _mapping(payload.get("main"))
    wind = _mapping(payload.get("wind"))
    system = _mapping(payload.get("sys"))
    weather_items = payload.get("weather")
    weather = _mapping(weather_items[0]) if isinstance(weather_items, list) and weather_items else {}
    return {
        "location": payload.get("name"),
        "country": system.get("country"),
        "observed_at": payload.get("dt"),
        "temperature_c": to_float(main.get("temp")),
        "feels_like_c": to_float(main.get("feels_like")),
        "humidity_percent": to_float(main.get("humidity")),
        "pressure_hpa": to_float(main.get("pressure")),
        "rainfall_mm": _rainfall(payload),
        "wind_speed_mps": to_float(wind.get("speed")),
        "weather": weather.get("main"),
        "description": weather.get("description"),
    }


def _has_current_measurements(data: dict) -> bool:
    required_fields = ("temperature_c", "humidity_percent", "wind_speed_mps")
    return all(data.get(field) is not None for field in required_fields)


def _normalize_forecast_item(item: dict) -> dict:
    main = _mapping(item.get("main"))
    wind = _mapping(item.get("wind"))
    weather_items = item.get("weather")
    weather = _mapping(weather_items[0]) if isinstance(weather_items, list) and weather_items else {}
    return {
        "forecast_at": item.get("dt"),
        "temperature_c": to_float(main.get("temp")),
        "humidity_percent": to_float(main.get("humidity")),
        "rainfall_mm": _rainfall(item, "3h"),
        "wind_speed_mps": to_float(wind.get("speed")),
        "weather": weather.get("main"),
        "description": weather.get("description"),
    }


def _has_forecast_measurements(data: dict) -> bool:
    required_fields = ("temperature_c", "humidity_percent", "wind_speed_mps")
    return all(data.get(field) is not None for field in required_fields)


def _fetch(
    endpoint: str,
    location: Optional[str],
    latitude: Optional[float],
    longitude: Optional[float],
    api_key: Optional[str],
    units: str,
    timeout: int,
    request_fn: Optional[RequestFunction],
) -> tuple[Optional[dict], Optional[dict]]:
    if units != "metric":
        return None, _error(
            "Only metric units are supported because normalized fields use Celsius and m/s.",
            "invalid_units",
        )
    timeout_value = to_float(timeout)
    if timeout_value is None or timeout_value <= 0:
        return None, _error("Timeout must be a positive number of seconds.", "invalid_timeout")
    key = _api_key(api_key)
    if not key:
        return None, _error(
            f"Set {API_KEY_ENVIRONMENT_VARIABLE} before requesting weather data.",
            "missing_api_key",
        )
    location_params, location_error = _location_parameters(location, latitude, longitude)
    if location_error:
        return None, location_error
    payload, request_error = _request_json(
        endpoint,
        {**_base_params(key, units), **(location_params or {})},
        timeout,
        request_fn,
    )
    return payload, request_error


def fetch_current_weather(
    location: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    api_key: Optional[str] = None,
    units: str = "metric",
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    request_fn: Optional[RequestFunction] = None,
) -> dict:
    """Fetch and normalize current weather by city or coordinates."""
    payload, error = _fetch(
        CURRENT_WEATHER_URL, location, latitude, longitude, api_key, units, timeout, request_fn
    )
    if error:
        return error
    data = _normalize_current(payload or {})
    if not _has_current_measurements(data):
        return _error("The weather API response was missing required measurements.", "missing_data")
    return {"status": "success", "data": data}


def fetch_forecast(
    location: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    api_key: Optional[str] = None,
    units: str = "metric",
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    request_fn: Optional[RequestFunction] = None,
) -> dict:
    """Fetch and normalize OpenWeatherMap's multi-period forecast."""
    payload, error = _fetch(
        FORECAST_URL, location, latitude, longitude, api_key, units, timeout, request_fn
    )
    if error:
        return error
    forecast_items = (payload or {}).get("list")
    if not isinstance(forecast_items, list):
        return _error("The forecast response did not contain forecast data.", "missing_data")
    normalized_forecast = []
    for item in forecast_items:
        if not isinstance(item, dict):
            continue
        normalized_item = _normalize_forecast_item(item)
        if _has_forecast_measurements(normalized_item):
            normalized_forecast.append(normalized_item)
    if not normalized_forecast:
        return _error("The forecast response did not contain usable forecast data.", "missing_data")
    city = _mapping((payload or {}).get("city"))
    return {
        "status": "success",
        "data": {
            "location": city.get("name"),
            "country": city.get("country"),
            "forecast": normalized_forecast,
        },
    }


# Conventional aliases keep the adapter easy to discover for future callers.
get_current_weather = fetch_current_weather
get_forecast = fetch_forecast
