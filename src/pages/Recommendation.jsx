import { useMemo } from 'react';

const recommendations = [
  {
    id: 1,
    title: 'Schedule Irrigation',
    description: 'Soil moisture remains below the recommended threshold for rice paddies.',
    priority: 'High',
    date: 'Aug 8, 2026',
    action: 'View Details',
  },
  {
    id: 2,
    title: 'Apply Fertilizer',
    description: 'Nitrogen levels could be improved after the next rainfall window.',
    priority: 'Medium',
    date: 'Aug 10, 2026',
    action: 'Mark as Done',
  },
  {
    id: 3,
    title: 'Inspect for Pests',
    description: 'Aphid risk increases in the north field after stagnant humidity.',
    priority: 'Low',
    date: 'Aug 12, 2026',
    action: 'View Details',
  },
];

function getStatusClass(priority) {
  return priority === 'High' ? 'status-high' : priority === 'Medium' ? 'status-medium' : 'status-low';
}

export default function Recommendation() {
  const recommendationList = useMemo(() => recommendations, []);

  return (
    <div className="recommendation-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">AI Recommendation Center</p>
          <h1 className="page-title">Operational guidance for your farm</h1>
          <p className="page-subtitle">Actionable advice for irrigation, fertilizer, pest control, and weather readiness.</p>
        </div>
      </div>

      <div className="grid-3">
        {recommendationList.map((item) => (
          <div key={item.id} className="card recommendation-detail-card">
            <div className="card-title-row">
              <h4>{item.title}</h4>
              <span className={`status-pill ${getStatusClass(item.priority)}`}>{item.priority}</span>
            </div>
            <p>{item.description}</p>
            <div className="recommendation-footer">
              <span>{item.date}</span>
              <button className="small-button primary-button">{item.action}</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
