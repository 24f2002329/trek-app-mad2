<template>
  <div class="container py-5 d-flex align-items-center justify-content-center" style="min-height: calc(80vh - 100px);">
    <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow-lg rounded-4 p-5 w-100" style="max-width: 480px;">
      <div class="text-center mb-4">
        <img src="../assets/images/logo.png" alt="Logo" class="mb-3" style="height: 64px; width: auto;" />
        <h2 class="fw-bold text-light">Create Account</h2>
        <p class="text-secondary small">Join TrekSphere as a Trekker</p>
      </div>

      <!-- Alert -->
      <div v-if="error" class="alert alert-danger bg-danger bg-opacity-10 border-danger border-opacity-20 text-danger small py-2 px-3 mb-4 rounded-3" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-1"></i> {{ error }}
      </div>
      <div v-if="success" class="alert alert-success bg-success bg-opacity-10 border-success border-opacity-20 text-success small py-2 px-3 mb-4 rounded-3" role="alert">
        <i class="bi bi-check-circle-fill me-1"></i> {{ success }}
      </div>

      <!-- Form -->
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="name" class="form-label text-secondary small fw-bold">Full Name</label>
          <input v-model="name" type="text" id="name" class="form-control bg-dark text-light border-secondary py-2" placeholder="Enter your full name (e.g. Jane Doe)" required />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label text-secondary small fw-bold">Email Address</label>
          <input v-model="email" type="email" id="email" class="form-control bg-dark text-light border-secondary py-2" placeholder="Enter your email (e.g. jane@domain.com)" required />
        </div>
        
        <div class="mb-4">
          <label for="password" class="form-label text-secondary small fw-bold">Password</label>
          <input v-model="password" type="password" id="password" class="form-control bg-dark text-light border-secondary py-2" placeholder="Create a password (minimum 6 characters)" required minlength="6" />
        </div>

        <button type="submit" class="btn btn-glow w-100 py-3 rounded-3" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          Create Account
        </button>
      </form>

      <div class="text-center mt-4 pt-2 border-top border-secondary border-opacity-10">
        <p class="text-secondary small mb-0">
          Already registered? 
          <router-link to="/login" class="text-gradient fw-bold text-decoration-none">Sign In</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '../services/api';

export default {
  name: 'Register',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      loading: false,
      error: '',
      success: ''
    };
  },
  methods: {
    async handleRegister() {
      this.loading = true;
      this.error = '';
      this.success = '';
      try {
        await authService.register(this.name, this.email, this.password);
        this.success = 'Registration successful! Redirecting to login...';
        setTimeout(() => {
          this.$router.push('/login');
        }, 1500);
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to register account. Try another email.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
