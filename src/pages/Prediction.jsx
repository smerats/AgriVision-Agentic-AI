import ChartComponent from '../components/ChartComponent.jsx';

const predictionData = {
  crop: 'Rice',
  predictedYield: 4.8,
  expectedHarvest: 'Sep 12, 2026',
  confidence: 89,
  previousSeasonChange: 8.4,
  factors: [
    { name: 'Weather', value: 82 },
    { name: 'Soil Health', value: 74 },
    { name: 'Crop Health', value: 89 },
    { name: 'Rainfall', value: 63 },
  ],
};

const history = [
  { period: '2022', yield: 3.9 },
  { period: '2023', yield: 4.2 },
  { period: '2024', yield: 4.5 },
  { period: '2025', yield: 4.6 },
  { period: '2026', yield: 4.8 },
];

export default function Prediction() {
  return (
    <div className="prediction-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Yield Prediction</p>
          <h1 className="page-title">Smart Harvest Forecast</h1>
          <p className="page-subtitle">AI-powered projections and trend drivers for your crop cycle.</p>
        </div>
      </div>

      <div className="grid-2">
        <div className="card prediction-summary-card">
          <h3>{predictionData.crop}</h3>
          <p className="stat-value">{predictionData.predictedYield} tons/hectare</p>
          <div className="prediction-meta">
            <div><span>Harvest date</span><strong>{predictionData.expectedHarvest}</strong></div>
            <div><span>Confidence</span><strong>{predictionData.confidence}%</strong></div>
          </div>
          <p className="increase-text">↑ {predictionData.previousSeasonChange}% from previous season</p>
        </div>
        <ChartComponent type="line" data={history} dataKey="yield" labelKey="period" title="Historical Yield" color="#4f7b58" />
      </div>

      <div className="card factors-card">
        <h4>Factors influencing prediction</h4>
        <div className="factor-list">
          {predictionData.factors.map((item) => (
            <div key={item.name} className="factor-row">
              <span>{item.name}</span>
              <div className="factor-bar"><div style={{ width: `${item.value}%` }} /></div>
              <strong>{item.value}%</strong>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
