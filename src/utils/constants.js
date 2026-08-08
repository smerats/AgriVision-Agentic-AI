export const NAV_ITEMS = [
  { path: '/dashboard', label: 'Dashboard', icon: 'Grid' },
  { path: '/weather', label: 'Weather', icon: 'CloudSun' },
  { path: '/crop-health', label: 'Crop Health', icon: 'Leaf' },
  { path: '/prediction', label: 'Prediction', icon: 'TrendingUp' },
  { path: '/recommendation', label: 'Recommendations', icon: 'Lightbulb' },
  { path: '/gis-map', label: 'GIS Map', icon: 'MapPin' },
  { path: '/profile', label: 'Profile', icon: 'User' },
  { path: '/settings', label: 'Settings', icon: 'SlidersHorizontal' }
];

export const WEATHER_CONDITIONS = ['Sunny', 'Partly Cloudy', 'Rainy', 'Stormy', 'Clear'];

export const RISK_LEVELS = {
  HIGH: 'High',
  MEDIUM: 'Medium',
  LOW: 'Low'
};

export const API_ENDPOINTS = {
  login: '/auth/login',
  register: '/auth/register',
  predictions: '/predictions',
  cropHealth: '/crop-health',
  risks: '/risks',
  recommendations: '/recommendations'
};

export const CROPS = ['Rice', 'Maize', 'Sugarcane', 'Vegetables', 'Coconut'];

export const APP_CONFIG = {
  defaultLocation: 'Kochi, Kerala',
  supportedUnits: ['Metric', 'Imperial']
};
