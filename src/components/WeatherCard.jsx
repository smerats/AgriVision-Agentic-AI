export default function WeatherCard({ weather }) {
  return (
    <div className="card weather-card">
      <div className="weather-card-header">
        <div>
          <p className="eyebrow">Current weather</p>
          <h2>{weather.temperature}°C</h2>
          <p className="weather-condition">{weather.condition}</p>
        </div>
        <div className="weather-icon">{weather.icon}</div>
      </div>
      <div className="weather-stats">
        <div>
          <p className="stat-label">Humidity</p>
          <p>{weather.humidity}%</p>
        </div>
        <div>
          <p className="stat-label">Wind</p>
          <p>{weather.wind} km/h</p>
        </div>
        <div>
          <p className="stat-label">Rain chance</p>
          <p>{weather.rainChance}%</p>
        </div>
      </div>
      <p className="weather-location">{weather.location}</p>
    </div>
  );
}
