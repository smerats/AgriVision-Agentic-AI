export default function SensorCard({ sensor }) {
  return (
    <div className="card sensor-card">
      <div className="sensor-row">
        <div>
          <p className="eyebrow">Soil Moisture</p>
          <h3>{sensor.soilMoisture}%</h3>
        </div>
        <div>
          <p className="eyebrow">Soil Temperature</p>
          <h3>{sensor.soilTemperature}°C</h3>
        </div>
      </div>
      <div className="sensor-row">
        <div>
          <p className="eyebrow">Soil pH</p>
          <h3>{sensor.soilPh}</h3>
        </div>
        <div>
          <p className="eyebrow">Air Temp</p>
          <h3>{sensor.airTemperature}°C</h3>
        </div>
      </div>
      <div className="sensor-row sensor-row-end">
        <div>
          <p className="eyebrow">Humidity</p>
          <h3>{sensor.humidity}%</h3>
        </div>
        <div>
          <p className="eyebrow">Light</p>
          <h3>{sensor.lightIntensity} lx</h3>
        </div>
      </div>
    </div>
  );
}
