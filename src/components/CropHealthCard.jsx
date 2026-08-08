export default function CropHealthCard({ data }) {
  return (
    <div className="card crop-health-card">
      <div className="card-title-row">
        <h3>{data.crop}</h3>
        <span className="badge">{data.status}</span>
      </div>
      <div className="health-summary">
        <div>
          <p className="eyebrow">Crop Health</p>
          <h2>{data.cropHealth}%</h2>
        </div>
        <div>
          <p className="eyebrow">NDVI</p>
          <h2>{data.ndvi}</h2>
        </div>
      </div>
      <div className="progress-row">
        <span>Health</span>
        <div className="progress-bar"><div style={{ width: `${data.cropHealth}%` }} /></div>
      </div>
      <p className="small-text">Last satellite scan: {data.lastScan}</p>
    </div>
  );
}
