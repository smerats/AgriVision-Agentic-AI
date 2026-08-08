export default function YieldCard({ data }) {
  return (
    <div className="card yield-card">
      <p className="eyebrow">Predicted Yield</p>
      <h3>{data.crop}</h3>
      <h2>{data.predictedYield} tons/hectare</h2>
      <div className="yield-meta">
        <div>
          <p className="stat-label">Expected harvest</p>
          <p>{data.expectedHarvest}</p>
        </div>
        <div>
          <p className="stat-label">Confidence</p>
          <p>{data.confidence}%</p>
        </div>
      </div>
      <p className="increase-text">↑ {data.previousSeasonChange}% from previous season</p>
    </div>
  );
}
