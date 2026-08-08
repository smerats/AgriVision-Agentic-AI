import { MapContainer, TileLayer, Marker, Popup, Polygon } from 'react-leaflet';
import { Icon } from 'leaflet';
import { useMemo } from 'react';

export default function MapComponent({ location, boundary, markers }) {
  const center = useMemo(() => [location.lat, location.lng], [location]);

  const farmIcon = new Icon({
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
    iconSize: [22, 34],
    iconAnchor: [11, 34],
  });

  return (
    <div className="card map-card">
      <div className="card-title-row">
        <h4>Farm GIS Overview</h4>
      </div>
      <MapContainer center={center} zoom={13} scrollWheelZoom={false} className="leaflet-map">
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Polygon positions={boundary} pathOptions={{ color: '#2d8fbc', weight: 2, fillOpacity: 0.08 }} />
        {markers.map((marker) => (
          <Marker key={marker.id} position={[marker.lat, marker.lng]} icon={farmIcon}>
            <Popup>{marker.label}</Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
