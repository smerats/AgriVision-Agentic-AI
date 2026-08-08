import { useEffect, useState } from 'react';
import WeatherCard from '../components/WeatherCard.jsx';
import CropHealthCard from '../components/CropHealthCard.jsx';
import YieldCard from '../components/YieldCard.jsx';
import RecommendationCard from '../components/RecommendationCard.jsx';
import RiskCard from '../components/RiskCard.jsx';
import SensorCard from '../components/SensorCard.jsx';
import ChartComponent from '../components/ChartComponent.jsx';
import MapComponent from '../components/MapComponent.jsx';
import { getCropHealth, getRecommendations, getRiskPrediction, getYieldPrediction } from '../services/predictionService.js';
import { getCurrentUser } from '../services/authService.js';

const weatherData = {
  temperature: 29,
  condition: 'Partly Cloudy',
  humidity: 78,
  wind: 12,
  rainChance: 35,
  location: 'Kochi, Kerala',
  icon: '☀️',
};

const sensorData = {
  soilMoisture: 62,
  soilTemperature: 27,
  soilPh: 6.5,
  airTemperature: 28,
  humidity: 78,
  lightIntensity: 14_500,
};

const tempTrend = [
  { day: 'Mon', temperature: 28 },
  { day: 'Tue', temperature: 30 },
  { day: 'Wed', temperature: 29 },
  { day: 'Thu', temperature: 27 },
  { day: 'Fri', temperature: 28 },
  { day: 'Sat', temperature: 29 },
  { day: 'Sun', temperature: 30 },
];

const rainfallTrend = [
  { day: 'Mon', rainfall: 12 },
  { day: 'Tue', rainfall: 18 },
  { day: 'Wed', rainfall: 10 },
  { day: 'Thu', rainfall: 8 },
  { day: 'Fri', rainfall: 23 },
  { day: 'Sat', rainfall: 16 },
  { day: 'Sun', rainfall: 12 },
];

const farmLocation = { lat: 9.9391, lng: 76.2705 };
const farmBoundary = [
  [9.941, 76.268],
  [9.942, 76.273],
  [9.937, 76.275],
  [9.936, 76.269],
];
const farmMarkers = [
  { id: 'field-1', lat: 9.9395, lng: 76.272, label: 'Field 1' },
  { id: 'sensor-1', lat: 9.938, lng: 76.27, label: 'Sensor' },
];

export default function Dashboard() {
  const [cropHealth, setCropHealth] = useState(null);
  const [yieldData, setYieldData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [risks, setRisks] = useState([]);
  const user = getCurrentUser();

  useEffect(() => {
    getCropHealth().then(setCropHealth);
    getYieldPrediction().then(setYieldData);
    getRecommendations().then(setRecommendations);
    getRiskPrediction().then(setRisks);
  }, []);

  return (
    <div className="dashboard-page">
      <section className="page-header">
        <div>
          <p className="eyebrow">Welcome back, Farmer 👋</p>
          <h1 className="page-title">{user?.name || 'Farmer'}</h1>
          <p className="page-subtitle">{user?.location || 'Kochi, Kerala'} • Last updated: Today</p>
        </div>
      </section>

      <div className="grid-4">
        <div className="card stat-card">
          <p className="stat-label">Temperature</p>
          <h3>{weatherData.temperature}°C</h3>
        </div>
        <div className="card stat-card">
          <p className="stat-label">Humidity</p>
          <h3>{weatherData.humidity}%</h3>
        </div>
        <div className="card stat-card">
          <p className="stat-label">Soil Moisture</p>
          <h3>{sensorData.soilMoisture}%</h3>
        </div>
        <div className="card stat-card">
          <p className="stat-label">Rain</p>
          <h3>{weatherData.rainChance}%</h3>
        </div>
      </div>

      <div className="grid-2">
        <WeatherCard weather={weatherData} />
        <CropHealthCard data={cropHealth || { crop: 'Rice', cropHealth: 0, ndvi: 0, status: 'Loading', lastScan: '...' }} />
      </div>

      <div className="grid-2">
        <YieldCard data={yieldData || { crop: 'Rice', predictedYield: 0, expectedHarvest: '-', confidence: 0, previousSeasonChange: 0 }} />
        <ChartComponent type="line" data={tempTrend} dataKey="temperature" labelKey="day" title="Temperature Trend" color="#2d8fbc" />
      </div>

      <section className="section-card">
        <div className="card-title-row">
          <h3>AI Recommendations</h3>
        </div>
        <div className="grid-3">
          {recommendations.map((item) => (
            <RecommendationCard key={item.id} recommendation={item} />
          ))}
        </div>
      </section>

      <section className="section-card">
        <div className="card-title-row">
          <h3>Farm Risk Alerts</h3>
        </div>
        <div className="grid-3">
          {risks.map((risk) => (
            <RiskCard key={risk.label} risk={risk} />
          ))}
        </div>
      </section>

      <section className="section-card">
        <div className="card-title-row">
          <h3>Sensor Monitoring</h3>
        </div>
        <SensorCard sensor={sensorData} />
      </section>

      <section className="section-card">
        <div className="grid-2">
          <ChartComponent type="area" data={rainfallTrend} dataKey="rainfall" labelKey="day" title="Rainfall Forecast" color="#3a7d96" />
          <MapComponent location={farmLocation} boundary={farmBoundary} markers={farmMarkers} />
        </div>
      </section>
    </div>
  );
}
