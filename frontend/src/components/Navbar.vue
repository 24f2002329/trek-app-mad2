<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark bg-opacity-75 border-bottom border-secondary border-opacity-25 shadow-sm sticky-top py-3">
    <div class="container">
      <router-link class="navbar-brand d-flex align-items-center fw-bold fs-4 text-gradient" to="/">
        <img src="../assets/images/logo.png" alt="Logo" class="me-2" style="height: 32px; width: auto;" /> TrekSphere
        <span class="ms-2 d-inline-block rounded-circle status-dot" :class="isOffline ? 'bg-danger text-danger' 
          : 'bg-success text-success'" style="width: 8px; height: 8px; margin-top: 4px;" :title="isOffline ? 'System Offline' : 'System Online'">
        </span>
      </router-link>
      
      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center gap-2">
          <li class="nav-item">
            <router-link class="nav-link px-3 text-secondary text-hover-light" to="/public-dashboard">Analytics</router-link>
          </li>
          <!-- Guest Navigation -->
          <template v-if="!isLoggedIn">
            <li class="nav-item">
              <router-link class="nav-link px-3 text-secondary text-hover-light" to="/">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 text-secondary text-hover-light" to="/treks">Browse Treks</router-link>
            </li>
            <li class="nav-item ms-lg-2">
              <router-link class="btn btn-outline-secondary px-4 py-2 border-secondary text-light" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="btn btn-glow px-4 py-2" to="/register">Register</router-link>
            </li>
          </template>
          
          <!-- Authenticated Navigation -->
          <template v-else>
            <li class="nav-item d-none d-lg-inline-block">
              <span class="text-secondary me-3">Logged in as: <strong class="text-light">{{ user?.name }}</strong> ({{ userRoleLabel }})</span>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 text-secondary text-hover-light" :to="dashboardPath">Dashboard</router-link>
            </li>
            <li class="nav-item ms-lg-2">
              <button @click="logout" class="btn btn-outline-secondary px-4 py-2 border-secondary text-light">Logout</button>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { authService, publicService } from '../services/api';

export default {
  name: 'Navbar',
  data() {
    return {
      isLoggedIn: false,
      user: null,
      isOffline: false
    };
  },
  computed: {
    dashboardPath() {
      if (!this.user) return '/';
      if (this.user.role === 'admin') return '/admin/dashboard';
      if (this.user.role === 'trek_staff') return '/staff/dashboard';
      return '/dashboard';
    },
    userRoleLabel() {
      if (!this.user) return '';
      if (this.user.role === 'admin') return 'Admin';
      if (this.user.role === 'trek_staff') return 'Staff';
      return 'Trekker';
    }
  },
  methods: {
    checkAuth() {
      this.isLoggedIn = authService.isAuthenticated();
      this.user = authService.getCurrentUser();
    },
    logout() {
      authService.logout();
      this.checkAuth();
      this.$router.push('/');
    },
    async checkSystemStatus() {
      try {
        const data = await publicService.getSystemStatus();
        this.isOffline = data.status !== 'online';
      } catch (err) {
        this.isOffline = true;
      }
    }
  },
  mounted() {
    this.checkAuth();
    this.checkSystemStatus();
    this.$watch(
      () => this.$route.path,
      () => {
        this.checkAuth();
        this.checkSystemStatus();
      }
    );
  }
}
</script>

<style scoped>
.text-hover-light:hover {
  color: #fff !important;
}
.router-link-exact-active {
  color: #00f2fe !important;
}
.status-dot {
  box-shadow: 0 0 8px currentColor;
  animation: blink 2.5s infinite ease-in-out;
}
@keyframes blink {
  0% { opacity: 0.45; }
  50% { opacity: 1; }
  100% { opacity: 0.45; }
}
</style>
