import ChartComponent from '../components/ChartComponent.jsx';

const weatherOverview = {
  current: 29,
  condition: 'Partly Cloudy',
  humidity: 78,
  wind: 12,
  uvIndex: 6,
  alert: 'Light rain expected tonight',
};

const forecast = [
  { day: 'Mon', temp: 30, rain: 18 },
  { day: 'Tue', temp: 29, rain: 12 },
  { day: 'Wed', temp: 28, rain: 6 },
  { day: 'Thu', temp: 27, rain: 14 },
  { day: 'Fri', temp: 28, rain: 20 },
  { day: 'Sat', temp: 29, rain: 16 },
  { day: 'Sun', temp: 30, rain: 10 },
];

export default function Weather() {
  return (
    <div className="weather-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Weather Intelligence</p>
          <h1 className="page-title">Kochi Local Forecast</h1>
          <p className="page-subtitle">Seven-day outlook and risk alerts for your farm.</p>
        </div>
      </div>

      <div className="grid-2">
        <div className="card weather-summary-card">
          <h3>{weatherOverview.current}°C</h3>
          <p className="weather-condition-large">{weatherOverview.condition}</p>
          <div className="weather-grid">
            <div><span>Humidity</span><strong>{weatherOverview.humidity}%</strong></div>
            <div><span>Wind</span><strong>{weatherOverview.wind} km/h</strong></div>
            <div><span>UV Index</span><strong>{weatherOverview.uvIndex}</strong></div>
            <div><span>Alert</span><strong>{weatherOverview.alert}</strong></div>
          </div>
        </div>
        <ChartComponent type="line" data={forecast} dataKey="temp" labelKey="day" title="Temperature Trend" color="#2d8fbc" />
      </div>

      <div className="grid-2">
        <ChartComponent type="bar" data={forecast} dataKey="rain" labelKey="day" title="Rainfall Forecast" color="#4a91a7" />
        <div className="card stats-card">
          <h4>Weather insights</h4>
          <div className="insight-row"><p>Cloud cover is moderate</p></div>
          <div className="insight-row"><p>Wind remains stable between 10-14 km/h</p></div>
          <div className="insight-row"><p>Schedule planting after Saturday rain clears</p></div>
        </div>
      </div>
    </div>
  );
}
