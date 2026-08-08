const AUTH_KEY = 'agritwin_user';

function getStoredUser() {
  const raw = localStorage.getItem(AUTH_KEY);
  return raw ? JSON.parse(raw) : null;
}

export function login(email, password) {
  const mockUser = {
    name: 'Farmer Asha',
    email,
    location: 'Kochi, Kerala',
    farmSize: '2.5 acres',
    mainCrop: 'Rice',
    token: 'demo-token',
  };
  localStorage.setItem(AUTH_KEY, JSON.stringify(mockUser));
  return mockUser;
}

export function register(userData) {
  const newUser = {
    name: userData.fullName || 'Farmer Partner',
    email: userData.email,
    location: userData.farmLocation || 'Kochi, Kerala',
    farmSize: '2.5 acres',
    mainCrop: userData.cropType || 'Rice',
    token: 'demo-token',
  };
  localStorage.setItem(AUTH_KEY, JSON.stringify(newUser));
  return newUser;
}

export function logout() {
  localStorage.removeItem(AUTH_KEY);
}

export function getCurrentUser() {
  return getStoredUser();
}

export function isAuthenticated() {
  return Boolean(getStoredUser()?.token);
}
