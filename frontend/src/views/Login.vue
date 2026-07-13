<template>
  <div class="container py-5 d-flex align-items-center justify-content-center" style="min-height: calc(80vh - 100px);">
    <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow-lg rounded-4 p-5 w-100" style="max-width: 480px;">
      <div class="text-center mb-4">
        <img src="../assets/images/logo.png" alt="Logo" class="mb-3" style="height: 64px; width: auto;" />
        <h2 class="fw-bold text-light">Welcome Back</h2>
        <p class="text-secondary small">Access your TrekSphere account</p>
      </div>

      <!-- Alert -->
      <div v-if="error" class="alert alert-danger bg-danger bg-opacity-10 border-danger border-opacity-20 text-danger small py-2 px-3 mb-4 rounded-3" role="alert">
        ⚠️ {{ error }}
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label text-secondary small fw-bold">Email Address</label>
          <input v-model="email" type="email" id="email" class="form-control bg-dark text-light border-secondary py-2" placeholder="Enter your email (e.g. admin@trek.com)" required />
        </div>
        
        <div class="mb-4">
          <div class="d-flex justify-content-between mb-1">
            <label for="password" class="form-label text-secondary small fw-bold mb-0">Password</label>
          </div>
          <input v-model="password" type="password" id="password" class="form-control bg-dark text-light border-secondary py-2" placeholder="Enter your password (e.g. admin123)" required />
        </div>

        <button type="submit" class="btn btn-glow w-100 py-3 rounded-3" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          Sign In
        </button>
      </form>

      <div class="text-center mt-4 pt-2 border-top border-secondary border-opacity-10">
        <p class="text-secondary small mb-0">
          Don't have an account yet? 
          <router-link to="/register" class="text-gradient fw-bold text-decoration-none">Register Now</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '../services/api';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: ''
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = '';
      try {
        const response = await authService.login(this.email, this.password);
        const redirectPath = this.$route.query.redirect || response.redirect;
        this.$router.push(redirectPath);
      } catch (err) {
        this.error = err.response?.data?.message || 'Invalid email or password. Please try again.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
