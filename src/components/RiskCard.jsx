export default function RiskCard({ risk }) {
  return (
    <div className={`card risk-card ${risk.status === 'warning' ? 'risk-warning' : risk.status === 'medium' ? 'risk-medium' : 'risk-low'}`}>
      <div className="risk-row">
        <span>{risk.status === 'warning' ? '⚠' : risk.status === 'medium' ? '⚠' : '✓'}</span>
        <div>
          <h4>{risk.label}</h4>
          <p>Probability: {risk.probability}%</p>
        </div>
      </div>
    </div>
  );
}
