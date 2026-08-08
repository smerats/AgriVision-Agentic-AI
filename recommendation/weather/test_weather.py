"""Tests for agricultural recommendations using mock weather data only."""

import unittest

from .forecast import generate_recommendations


class WeatherRecommendationTests(unittest.TestCase):
    """Verify the exact recommendation output contract with mock weather data."""

    def recommendations_for(self, current, forecast=None):
        weather_data = {"current": current}
        if forecast is not None:
            weather_data["forecast"] = forecast
        return generate_recommendations(weather_data)

    @staticmethod
    def assert_output_shape(test_case, result):
        test_case.assertEqual(set(result), {"weather_status", "risk", "recommendations"})
        test_case.assertIn(result["risk"], {"low", "moderate", "high"})
        test_case.assertIsInstance(result["recommendations"], list)
        test_case.assertTrue(all(isinstance(item, str) for item in result["recommendations"]))

    def test_normal_weather(self):
        result = self.recommendations_for(
            {
                "temperature_c": 28,
                "rainfall_mm": 12,
                "humidity_percent": 60,
                "wind_speed_mps": 3,
            }
        )

        self.assert_output_shape(self, result)
        self.assertEqual(result["weather_status"], "normal")
        self.assertEqual(result["risk"], "low")

    def test_heavy_rainfall_recommends_pausing_irrigation_and_fertilizer(self):
        result = self.recommendations_for(
            {
                "temperature_c": 24,
                "rainfall_mm": 30,
                "humidity_percent": 85,
                "wind_speed_mps": 4,
            }
        )

        self.assert_output_shape(self, result)
        self.assertEqual(result["weather_status"], "rain_expected")
        self.assertEqual(result["risk"], "high")
        self.assertIn("Avoid irrigation today.", result["recommendations"])
        self.assertIn("Delay fertilizer application until rainfall decreases.", result["recommendations"])
        self.assertIn("Monitor the field for waterlogging.", result["recommendations"])

    def test_high_temperature_with_low_rainfall_recommends_irrigation(self):
        result = self.recommendations_for(
            {
                "temperature_c": 37,
                "rainfall_mm": 2,
                "humidity_percent": 45,
                "wind_speed_mps": 4,
            }
        )

        self.assert_output_shape(self, result)
        self.assertEqual(result["weather_status"], "hot_and_dry")
        self.assertEqual(result["risk"], "high")
        self.assertTrue(any("irrigate" in item.lower() for item in result["recommendations"]))
        self.assertTrue(any("high temperatures" in item for item in result["recommendations"]))

    def test_strong_wind_limits_field_activities(self):
        result = self.recommendations_for(
            {
                "temperature_c": 26,
                "rainfall_mm": 10,
                "humidity_percent": 55,
                "wind_speed_mps": 12,
            }
        )

        self.assert_output_shape(self, result)
        self.assertEqual(result["weather_status"], "strong_wind")
        self.assertEqual(result["risk"], "high")
        self.assertTrue(any("strong winds" in item for item in result["recommendations"]))

    def test_very_low_temperature_limits_field_activities(self):
        result = self.recommendations_for(
            {
                "temperature_c": 5,
                "rainfall_mm": 10,
                "humidity_percent": 55,
                "wind_speed_mps": 3,
            }
        )

        self.assert_output_shape(self, result)
        self.assertEqual(result["weather_status"], "low_temperature")
        self.assertEqual(result["risk"], "moderate")
        self.assertTrue(any("low temperatures" in item for item in result["recommendations"]))

    def test_missing_weather_values_return_structured_error(self):
        result = self.recommendations_for(
            {
                "temperature_c": None,
                "rainfall_mm": None,
                "humidity_percent": None,
                "wind_speed_mps": None,
            }
        )

        self.assert_output_shape(self, result)
        self.assertEqual(result["weather_status"], "unknown")
        self.assertEqual(result["risk"], "high")
        self.assertEqual(len(result["recommendations"]), 1)


if __name__ == "__main__":
    unittest.main()
