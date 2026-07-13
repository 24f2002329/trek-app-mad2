import axios from 'axios';

const api = axios.create({
  baseURL: '', // Proxied automatically by Vite to Flask backend
  headers: {
    'Content-Type': 'application/json'
  }
});

// Attach JWT token to requests if present in localStorage
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercept unauthorized responses to force log out
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      // If we aren't already on login, send the user there
      if (window.location.pathname !== '/login' && window.location.pathname !== '/' && window.location.pathname !== '/treks') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authService = {
  async login(email, password) {
    const response = await api.post('/api/auth/login', { email, password });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },
  async register(name, email, password) {
    const response = await api.post('/api/auth/register', { name, email, password });
    return response.data;
  },
  async getMe() {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },
  isAuthenticated() {
    return !!localStorage.getItem('token');
  }
};

export const publicService = {
  async getStats() {
    const response = await api.get('/api/public/stats');
    return response.data;
  },
  async getTreks(params) {
    const response = await api.get('/api/public/treks', { params });
    return response.data;
  },
  async getTrekDetail(id) {
    const response = await api.get(`/api/public/treks/${id}`);
    return response.data;
  }
};

export const adminService = {
  async getDashboardSummary() {
    const response = await api.get('/api/admin/dashboard-summary');
    return response.data;
  }
};

export const staffService = {
  async getDashboardSummary() {
    const response = await api.get('/api/staff/dashboard-summary');
    return response.data;
  },
  async updateTrekStatus(trekId, status) {
    const response = await api.put(`/api/staff/treks/${trekId}/status`, { status });
    return response.data;
  }
};

export const userService = {
  async getDashboardSummary() {
    const response = await api.get('/api/user/dashboard-summary');
    return response.data;
  },
  async createBooking(trekId, slots = 1) {
    const response = await api.post('/api/booking/bookings', { trek_id: trekId, slots });
    return response.data;
  }
};

export default api;
