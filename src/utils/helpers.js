export function formatDateLabel(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-IN', {
    month: 'short',
    day: 'numeric',
  });
}

export function formatTemperature(value) {
  return `${value}°C`;
}

export function formatPercent(value) {
  return `${value}%`;
}

export function getRiskClass(status) {
  if (status === 'warning') return 'status-high';
  if (status === 'medium') return 'status-medium';
  return 'status-low';
}

export function getHealthStatus(value) {
  if (value >= 85) return 'Healthy';
  if (value >= 70) return 'Monitor';
  return 'At risk';
}

export function formatNumber(value, digits = 1) {
  return Number(value).toFixed(digits);
}
