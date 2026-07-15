import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',       // proxied automatically by Vite to flask backend or configured custom base URL
  headers: {
    'Content-Type': 'application/json'
  }
});


// attach jwt token to requests if present in localstorage
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

// intercept unauthorized responses to force log out
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      // if we aren't already on login, send the user there
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
  },
  async getSystemStatus() {
    const response = await api.get('/api/public/system-status');
    return response.data;
  }
};

export const adminService = {
  async getDashboardSummary() {
    const response = await api.get('/api/admin/dashboard-summary');
    return response.data;
  },
  async getSystemStatus() {
    const response = await api.get('/api/admin/system-status');
    return response.data;
  },
  async getTreks(params) {
    const response = await api.get('/api/admin/treks', { params });
    return response.data;
  },
  async createTrek(data) {
    const response = await api.post('/api/admin/treks', data);
    return response.data;
  },
  async updateTrek(id, data) {
    const response = await api.put(`/api/admin/treks/${id}`, data);
    return response.data;
  },
  async closeBooking(trekId) {
    const response = await api.put(`/api/staff/treks/${trekId}/close-booking`);
    return response.data;
  },
  async deleteTrek(id) {
    const response = await api.delete(`/api/admin/treks/${id}`);
    return response.data;
  },
  async getStaff(params) {
    const response = await api.get('/api/admin/staff', { params });
    return response.data;
  },
  async createStaff(data) {
    const response = await api.post('/api/admin/staff', data);
    return response.data;
  },
  async updateStaff(id, data) {
    const response = await api.put(`/api/admin/staff/${id}`, data);
    return response.data;
  },
  async toggleStaffStatus(id, isActive) {
    const response = await api.put(`/api/admin/staff/${id}/status`, { is_active: isActive });
    return response.data;
  },
  async getUsers(params) {
    const response = await api.get('/api/admin/users', { params });
    return response.data;
  },
  async toggleUserStatus(id, isActive) {
    const response = await api.put(`/api/admin/users/${id}/status`, { is_active: isActive });
    return response.data;
  },
  async getBookings(params) {
    const response = await api.get('/api/admin/bookings', { params });
    return response.data;
  },
  async updateBookingStatus(id, status) {
    const response = await api.put(`/api/admin/bookings/${id}/status`, { status });
    return response.data;
  },
  async getReportStats() {
    const response = await api.get('/api/admin/reports/stats');
    return response.data;
  },
  async getUserDetail(userId) {
    const response = await api.get(`/api/admin/users/${userId}`);
    return response.data;
  },
  async updateUserDetail(userId, data) {
    const response = await api.put(`/api/admin/users/${userId}`, data);
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
  },
  async closeBooking(trekId) {
    const response = await api.put(`/api/staff/treks/${trekId}/close-booking`);
    return response.data;
  },
  async updateTrekSlots(trekId, maxSlots) {
    const response = await api.put(`/api/staff/treks/${trekId}/slots`, { max_slots: maxSlots });
    return response.data;
  },
  async updateBookingStatus(bookingId, status) {
    const response = await api.put(`/api/staff/bookings/${bookingId}/status`, { status });
    return response.data;
  },
  async getProfile() {
    const response = await api.get('/api/staff/profile');
    return response.data;
  },
  async updateProfile(data) {
    const response = await api.put('/api/staff/profile', data);
    return response.data;
  },
  async getSystemStatus() {
    const response = await api.get('/api/staff/system-status');
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
  },
  async getProfile() {
    const response = await api.get('/api/user/profile');
    return response.data;
  },
  async updateProfile(data) {
    const response = await api.put('/api/user/profile', data);
    return response.data;
  },
  async cancelBooking(bookingId) {
    const response = await api.post(`/api/booking/bookings/${bookingId}/cancel`);
    return response.data;
  },
  async triggerCSVExport() {
    const response = await api.post('/api/user/export-history');
    return response.data;
  },
  async triggerBookingsCSVExport() {
    const response = await api.post('/api/user/export-bookings');
    return response.data;
  },
  async getExportStatus(taskId) {
    const response = await api.get(`/api/user/export-status/${taskId}`);
    return response.data;
  },
  async payBooking(bookingId) {
    const response = await api.post(`/api/booking/bookings/${bookingId}/pay`);
    return response.data;
  }
};

export default api;
