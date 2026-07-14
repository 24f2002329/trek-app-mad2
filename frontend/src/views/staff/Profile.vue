<template>
  <DashboardLayout role="staff">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">My <span class="text-gradient">Guide Profile</span></h1>
        <p class="text-secondary mb-0">Update your public profile, contact details, experience stats, and technical climbing bio.</p>
      </div>
    </div>

    <!-- Profile Form Card -->
    <div class="row g-4 justify-content-center">
      <div class="col-lg-8">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 p-md-5">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <form v-else @submit.prevent="saveProfile">
            <!-- Header Avatar Summary -->
            <div class="d-flex flex-column flex-sm-row align-items-center gap-4 mb-5 pb-4 border-bottom border-secondary border-opacity-15">
              <div class="avatar-lg bg-gradient text-white fw-bold rounded-circle d-flex align-items-center justify-content-center">
                {{ userInitial }}
              </div>
              <div class="text-center text-sm-start">
                <h4 class="fw-bold text-light mb-1">{{ profile.name }}</h4>
                <div class="text-secondary small mb-2"><i class="bi bi-envelope"></i> {{ profile.email }}</div>
                <div class="d-flex flex-wrap justify-content-center justify-content-sm-start gap-2">
                  <span class="badge bg-secondary bg-opacity-25 border border-secondary border-opacity-50 text-light">{{ profile.experience_years }} Yrs Experience</span>
                </div>
              </div>
            </div>

            <!-- Fields -->
            <div class="row g-4">
              <div class="col-md-6">
                <label class="form-label text-secondary small">Full Name *</label>
                <input v-model="profile.name" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light py-2 px-3" placeholder="e.g. Ravi Kumar" required />
              </div>

              <div class="col-md-6">
                <label class="form-label text-secondary small">Email Address</label>
                <input :value="profile.email" type="email" class="form-control bg-black bg-opacity-20 border-secondary text-secondary py-2 px-3" disabled />
                <div class="form-text text-muted" style="font-size: 0.7rem;">Email address cannot be changed.</div>
              </div>

              <div class="col-md-6">
                <label class="form-label text-secondary small">Contact Phone</label>
                <input v-model="profile.contact" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light py-2 px-3" placeholder="e.g. 9876543210" />
              </div>

              <div class="col-md-6">
                <label class="form-label text-secondary small">Experience (Years)</label>
                <input v-model.number="profile.experience_years" type="number" min="0" class="form-control bg-black bg-opacity-25 border-secondary text-light py-2 px-3" placeholder="0" />
              </div>

              <div class="col-12">
                <label class="form-label text-secondary small">Skills (Comma-separated)</label>
                <input v-model="profile.skills" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light py-2 px-3" placeholder="e.g. First Aid, Glacier Travel, High Altitude Navigation" />
              </div>

              <div class="col-12">
                <label class="form-label text-secondary small">Short Professional Bio</label>
                <textarea v-model="profile.bio" rows="4" class="form-control bg-black bg-opacity-25 border-secondary text-light py-2 px-3" placeholder="Describe your trek leadership style, mountains climbed, and safety record..."></textarea>
              </div>
            </div>

            <!-- Submit -->
            <div class="d-flex justify-content-end mt-5 pt-4 border-top border-secondary border-opacity-15">
              <button type="submit" class="btn btn-glow px-5 py-2 rounded-3" :disabled="submitting">
                <span v-if="submitting" class="spinner-border spinner-border-sm me-1" role="status"></span>
                Save Profile Changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import { staffService } from '../../services/api';
import { alertService } from '@/services/alert';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'StaffProfile',
  components: {
    DashboardLayout
  },
  data() {
    return {
      profile: {
        name: '',
        email: '',
        contact: '',
        experience_years: 0,
        skills: '',
        bio: '',
        is_active: true
      },
      loading: true,
      submitting: false
    };
  },
  computed: {
    userInitial() {
      return this.profile.name ? this.profile.name.charAt(0).toUpperCase() : 'G';
    }
  },
  methods: {
    async fetchProfile() {
      this.loading = true;
      try {
        const data = await staffService.getProfile();
        this.profile = data;
      } catch (err) {
        console.error('Failed to load profile', err);
      } finally {
        this.loading = false;
      }
    },
    async saveProfile() {
      this.submitting = true;
      try {
        await staffService.updateProfile({
          name: this.profile.name,
          contact: this.profile.contact,
          experience_years: this.profile.experience_years,
          skills: this.profile.skills,
          bio: this.profile.bio
        });
        alertService.success('Profile saved successfully!');
        
        // Update name in localstorage if it changed so the navbar updates instantly
        const userStr = localStorage.getItem('user');
        if (userStr) {
          const user = JSON.parse(userStr);
          user.name = this.profile.name;
          localStorage.setItem('user', JSON.stringify(user));
        }
        
        this.fetchProfile();
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Failed to update profile.');
      } finally {
        this.submitting = false;
      }
    }
  },
  mounted() {
    this.fetchProfile();
  }
}
</script>

<style scoped>
.avatar-lg {
  width: 72px;
  height: 72px;
  font-size: 2rem;
  background: linear-gradient(135deg, #00f2fe, #4facfe);
  flex-shrink: 0;
  box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
}
</style>
