import ChartComponent from '../components/ChartComponent.jsx';

const cropData = {
  cropHealth: 87,
  ndvi: 0.72,
  vegetationCondition: 'Healthy',
  lastScan: '2 hours ago',
};

const trend = [
  { day: 'Mon', health: 82 },
  { day: 'Tue', health: 84 },
  { day: 'Wed', health: 86 },
  { day: 'Thu', health: 87 },
  { day: 'Fri', health: 88 },
  { day: 'Sat', health: 87 },
  { day: 'Sun', health: 89 },
];

export default function CropHealth() {
  return (
    <div className="crop-health-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Crop Health Analytics</p>
          <h1 className="page-title">Vegetation Condition Monitor</h1>
          <p className="page-subtitle">Satellite insights, NDVI trends, and field risk warnings.</p>
        </div>
      </div>

      <div className="grid-3">
        <div className="card large-stat-card">
          <h3>Crop Health</h3>
          <p className="stat-value">{cropData.cropHealth}%</p>
          <p className="text-muted">Rice health rating based on satellite imagery.</p>
        </div>
        <div className="card large-stat-card">
          <h3>NDVI</h3>
          <p className="stat-value">{cropData.ndvi}</p>
          <p className="text-muted">Vegetation density is stable and healthy.</p>
        </div>
        <div className="card large-stat-card">
          <h3>Last Scan</h3>
          <p className="stat-value">{cropData.lastScan}</p>
          <p className="text-muted">Next satellite pass in 4 hours.</p>
        </div>
      </div>

      <div className="grid-2">
        <ChartComponent type="line" data={trend} dataKey="health" labelKey="day" title="Historical Health Trend" color="#347a47" />
        <div className="card analysis-card">
          <h4>Potential concerns</h4>
          <ul>
            <li>Monitor northern block for leaf spot.</li>
            <li>Soil moisture remains adequate in most sections.</li>
            <li>Maintain nutrient schedule over next 7 days.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
