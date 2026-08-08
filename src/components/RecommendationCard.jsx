export default function RecommendationCard({ recommendation }) {
  return (
    <div className="card recommendation-card">
      <div className="card-title-row">
        <h4>{recommendation.title}</h4>
        <span className={`status-pill ${recommendation.priority === 'High' ? 'status-high' : recommendation.priority === 'Medium' ? 'status-medium' : 'status-low'}`}>
          {recommendation.priority}
        </span>
      </div>
      <p className="recommendation-message">{recommendation.message}</p>
      <div className="recommendation-meta">
        <span>{recommendation.date}</span>
        <span className="action-pill">{recommendation.action}</span>
      </div>
    </div>
  );
}
