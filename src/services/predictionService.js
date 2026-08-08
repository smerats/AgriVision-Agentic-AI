import { apiRequest } from './api.js';

const mockYield = {
  crop: 'Rice',
  predictedYield: 4.8,
  expectedHarvest: 'Sep 12, 2026',
  confidence: 89,
  previousSeasonChange: 8.4,
  factors: [
    { label: 'Weather', value: 82 },
    { label: 'Soil Health', value: 74 },
    { label: 'Crop Health', value: 89 },
    { label: 'Rainfall', value: 63 },
  ],
};

const mockHealth = {
  cropHealth: 87,
  ndvi: 0.72,
  vegetationCondition: 'Healthy',
  lastScan: '2 hours ago',
  healthTrend: [
    { day: 'Mon', health: 82 },
    { day: 'Tue', health: 85 },
    { day: 'Wed', health: 86 },
    { day: 'Thu', health: 87 },
    { day: 'Fri', health: 88 },
    { day: 'Sat', health: 87 },
    { day: 'Sun', health: 89 },
  ],
};

const mockRisk = [
  { label: 'Heavy Rain Risk', probability: 72, status: 'warning' },
  { label: 'Pest Risk', probability: 38, status: 'medium' },
  { label: 'Drought Risk', probability: 12, status: 'low' },
];

const mockRecommendations = [
  {
    id: 1,
    title: 'Irrigation Recommended',
    message: 'Soil moisture is below optimal level. Consider irrigation within the next 12 hours.',
    priority: 'High',
    date: 'Aug 8, 2026',
    action: 'Start irrigation cycle',
  },
  {
    id: 2,
    title: 'Fertilizer Planning',
    message: 'Apply nitrogen-rich fertilizer after the next rainfall window.',
    priority: 'Medium',
    date: 'Aug 10, 2026',
    action: 'Schedule application',
  },
  {
    id: 3,
    title: 'Pest Scout',
    message: 'Monitor leaf damage in the northern block for potential aphid activity.',
    priority: 'Low',
    date: 'Aug 12, 2026',
    action: 'Inspect field',
  },
];

export async function getYieldPrediction() {
  try {
    return await apiRequest('/predictions/yield');
  } catch {
    return mockYield;
  }
}

export async function getCropHealth() {
  try {
    return await apiRequest('/crop-health');
  } catch {
    return mockHealth;
  }
}

export async function getRiskPrediction() {
  try {
    return await apiRequest('/risks');
  } catch {
    return mockRisk;
  }
}

export async function getRecommendations() {
  try {
    return await apiRequest('/recommendations');
  } catch {
    return mockRecommendations;
  }
}
