<template>
  <DashboardLayout role="user">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Trekker <span class="text-gradient">Profile</span></h1>
        <p class="text-secondary mb-0">Manage your profile details, update credentials, and verify your account status.</p>
      </div>
    </div>

    <!-- Forms -->
    <div class="row g-4">
      <div class="col-lg-6">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow h-100">
          <h5 class="fw-bold text-light mb-4"><i class="bi bi-person-gear text-info me-2"></i>Personal Details</h5>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <form v-else @submit.prevent="updateProfile">
            <div class="mb-3">
              <label class="form-label text-secondary small">Email Address (Read-only)</label>
              <input 
                :value="user.email" 
                type="email" 
                class="form-control bg-black bg-opacity-25 border-secondary text-secondary py-2" 
                disabled 
              />
              <div class="form-text text-muted small">Your email is the unique identifier for your account.</div>
            </div>

            <div class="mb-4">
              <label class="form-label text-secondary small">Full Name</label>
              <input 
                v-model="form.name" 
                type="text" 
                class="form-control bg-black bg-opacity-25 border-secondary text-light py-2" 
                required 
                placeholder="Enter your full name"
              />
            </div>

            <button type="submit" class="btn btn-glow px-4 py-2 w-100" :disabled="submitting">
              <span v-if="submitting" class="spinner-border spinner-border-sm me-1" role="status"></span>
              Save General Changes
            </button>
          </form>
        </div>
      </div>

      <div class="col-lg-6">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow h-100">
          <h5 class="fw-bold text-light mb-4"><i class="bi bi-shield-lock text-warning me-2"></i>Security & Credentials</h5>

          <form @submit.prevent="updatePassword">
            <div class="mb-3">
              <label class="form-label text-secondary small">New Password</label>
              <input 
                v-model="passwordForm.password" 
                type="password" 
                class="form-control bg-black bg-opacity-25 border-secondary text-light py-2" 
                placeholder="Enter new password"
                required
              />
              <div class="form-text text-muted small">Must be at least 8 characters long.</div>
            </div>

            <div class="mb-4">
              <label class="form-label text-secondary small">Confirm New Password</label>
              <input 
                v-model="passwordForm.confirmPassword" 
                type="password" 
                class="form-control bg-black bg-opacity-25 border-secondary text-light py-2" 
                placeholder="Re-enter new password"
                required
              />
            </div>

            <button type="submit" class="btn btn-outline-warning w-100 py-2 rounded-3 fw-semibold" :disabled="submittingPassword">
              <span v-if="submittingPassword" class="spinner-border spinner-border-sm me-1" role="status"></span>
              Update Password
            </button>
          </form>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import { userService } from '../../services/api';
import { alertService } from '@/services/alert';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'UserProfile',
  components: {
    DashboardLayout
  },
  data() {
    return {
      user: {
        name: '',
        email: ''
      },
      form: {
        name: ''
      },
      passwordForm: {
        password: '',
        confirmPassword: ''
      },
      loading: true,
      submitting: false,
      submittingPassword: false
    };
  },
  methods: {
    async fetchProfile() {
      this.loading = true;
      try {
        const data = await userService.getProfile();
        this.user = data;
        this.form.name = data.name;
      } catch (err) {
        alertService.error('Failed to load profile details.');
      } finally {
        this.loading = false;
      }
    },
    async updateProfile() {
      if (!this.form.name.trim()) {
        alertService.error('Name cannot be empty.');
        return;
      }
      this.submitting = true;
      try {
        await userService.updateProfile({ name: this.form.name });
        alertService.success('Profile details updated successfully!');
        // Update user name local ref
        this.user.name = this.form.name;
        // Optionally update token storage if needed
        const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
        currentUser.name = this.form.name;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Failed to update profile.');
      } finally {
        this.submitting = false;
      }
    },
    async updatePassword() {
      if (this.passwordForm.password.length < 8) {
        alertService.error('Password must be at least 8 characters long.');
        return;
      }
      if (this.passwordForm.password !== this.passwordForm.confirmPassword) {
        alertService.error('Passwords do not match.');
        return;
      }
      
      this.submittingPassword = true;
      try {
        await userService.updateProfile({ password: this.passwordForm.password });
        alertService.success('Credentials upgraded successfully!');
        this.passwordForm.password = '';
        this.passwordForm.confirmPassword = '';
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Failed to update credentials.');
      } finally {
        this.submittingPassword = false;
      }
    }
  },
  mounted() {
    this.fetchProfile();
  }
}
</script>
