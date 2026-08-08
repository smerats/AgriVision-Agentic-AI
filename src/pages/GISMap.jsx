import MapComponent from '../components/MapComponent.jsx';

const farmLocation = { lat: 9.9391, lng: 76.2705 };
const farmBoundary = [
  [9.941, 76.268],
  [9.942, 76.273],
  [9.937, 76.275],
  [9.936, 76.269],
];
const markers = [
  { id: 1, lat: 9.9395, lng: 76.272, label: 'Main field' },
  { id: 2, lat: 9.938, lng: 76.27, label: 'Weather sensor' },
];

export default function GISMap() {
  return (
    <div className="gis-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">GIS & Satellite Monitoring</p>
          <h1 className="page-title">Farm Map Intelligence</h1>
          <p className="page-subtitle">Interactive field boundary, health overlay, and risk layer demo.</p>
        </div>
      </div>

      <div className="grid-2">
        <MapComponent location={farmLocation} boundary={farmBoundary} markers={markers} />
        <div className="card layer-controls-card">
          <h4>Map Layers</h4>
          <div className="layer-list">
            <label className="layer-row"><input type="checkbox" defaultChecked /> Farm Boundary</label>
            <label className="layer-row"><input type="checkbox" defaultChecked /> Crop Health</label>
            <label className="layer-row"><input type="checkbox" /> Soil Moisture</label>
            <label className="layer-row"><input type="checkbox" /> Risk Zones</label>
            <label className="layer-row"><input type="checkbox" /> Satellite imagery</label>
          </div>
          <div className="legend-block">
            <p className="subtitle">Legend</p>
            <div className="legend-item"><span className="legend-color" style={{ background: '#2d8fbc' }} /> Farm Boundary</div>
            <div className="legend-item"><span className="legend-color" style={{ background: '#4f7b58' }} /> Crop Health overlay</div>
            <div className="legend-item"><span className="legend-color" style={{ background: '#d9822b' }} /> Risk zones</div>
          </div>
        </div>
      </div>
    </div>
  );
}
