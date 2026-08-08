const API_URL = import.meta.env.VITE_API_URL || '';

export async function apiRequest(endpoint, options = {}) {
  const url = `${API_URL}${endpoint}`;
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data?.message || 'API request failed');
    }
    return data;
  } catch (error) {
    throw new Error(error.message || 'Network error');
  }
}
