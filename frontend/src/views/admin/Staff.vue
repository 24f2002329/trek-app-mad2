<template>
  <DashboardLayout role="admin">
    <!-- Header & Register Trigger -->
    <div class="row align-items-center mb-5">
      <div class="col-md-6 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Manage <span class="text-gradient">Staff Guides</span></h1>
        <p class="text-secondary mb-0">Register new guides, review credentials, or blacklist accounts</p>
      </div>
      <div class="col-md-6 text-center text-md-end mt-3 mt-md-0">
        <button @click="openCreateModal" class="btn btn-glow px-4 py-2">
          <i class="bi bi-person-plus-fill me-2"></i>Register Trek Leader
        </button>
      </div>
    </div>

    <!-- Search bar -->
    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 mb-4 shadow">
      <div class="row g-3">
        <div class="col-12">
          <div class="input-group">
            <span class="input-group-text bg-black bg-opacity-25 border-secondary text-secondary"><i class="bi bi-search"></i></span>
            <input 
              v-model="filters.search" 
              @input="fetchStaff" 
              type="text" 
              class="form-control bg-black bg-opacity-25 border-secondary text-light" 
              placeholder="Search by name, email, or ID..."
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Staff List -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-info" role="status"></div>
    </div>

    <div v-else-if="staffList.length === 0" class="card bg-dark bg-opacity-25 border-secondary border-opacity-10 text-center py-5">
      <span class="display-3 mb-2 d-block text-secondary"><i class="bi bi-person-badge-fill"></i></span>
      <p class="text-secondary mb-0">No staff members found.</p>
    </div>

    <div v-else class="row g-4">
      <div class="col-lg-6" v-for="staff in staffList" :key="staff.id">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100 position-relative hover-card">
          <div class="d-flex align-items-start gap-3">
            <div class="avatar bg-secondary bg-opacity-25 text-gradient fw-bold rounded-circle d-flex align-items-center justify-content-center fs-4" style="width: 54px; height: 54px;">
              {{ staff.name.charAt(0).toUpperCase() }}
            </div>
            <div class="overflow-hidden flex-grow-1">
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-info small fw-bold">ID: {{ staff.id }}</span>
                <span class="badge rounded-pill" :class="staff.is_active ? 'bg-success bg-opacity-25 text-success border border-success border-opacity-25' : 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25'">
                  {{ staff.is_active ? 'Active 🟢' : 'Deactivated 🔴' }}
                </span>
              </div>
              <h5 class="fw-bold text-light mb-1 mt-1">{{ staff.name }}</h5>
              <div class="text-secondary small mb-2"><i class="bi bi-envelope"></i> {{ staff.email }}</div>
              <div class="d-flex flex-wrap gap-2 mb-3">
                <span class="badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-50"><i class="bi bi-telephone"></i> {{ staff.contact || 'No Contact' }}</span>
                <span class="badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-50"><i class="bi bi-star"></i> {{ staff.experience_years }} Yrs Exp</span>
              </div>
            </div>
          </div>

          <div class="p-3 bg-black bg-opacity-25 rounded-3 mb-4 border border-secondary border-opacity-10 mt-2">
            <span class="text-secondary tiny-text d-block mb-1">SKILLS</span>
            <div class="text-light small text-truncate mb-2">{{ staff.skills || 'No skills listed' }}</div>
            <span class="text-secondary tiny-text d-block mb-1">BIO</span>
            <div class="text-secondary small text-line-clamp">{{ staff.bio || 'No bio listed' }}</div>
          </div>

          <div class="d-flex gap-3 justify-content-end border-top border-secondary border-opacity-10 pt-3 mt-auto">
            <button @click="toggleActiveStatus(staff)" class="btn btn-sm rounded-3 px-3" :class="staff.is_active ? 'btn-outline-danger' : 'btn-outline-success'">
              <i class="bi" :class="staff.is_active ? 'bi-lock-fill' : 'bi-unlock-fill'"></i>
              {{ staff.is_active ? 'Deactivate' : 'Activate' }}
            </button>
            <button @click="openEditModal(staff)" class="btn btn-outline-info btn-sm rounded-3 px-3">
              <i class="bi bi-pencil-square me-1"></i>Edit Profile
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bootstrap Modal for Register/Edit (Teleported to body to avoid stacking context issues) -->
    <Teleport to="body">
    <div class="modal fade" id="staffModal" tabindex="-1" aria-hidden="true" ref="staffModal">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content bg-dark text-light border border-secondary border-opacity-50 rounded-4">
          <div class="modal-header border-secondary border-opacity-25">
            <h5 class="modal-title fw-bold text-light">
              {{ isEdit ? 'Edit Staff Profile' : 'Register New Trek Leader' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="saveStaff">
            <div class="modal-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label text-secondary small">Full Name *</label>
                  <input v-model="form.name" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="e.g. Ravi Sharma" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label text-secondary small">Email Address *</label>
                  <input v-model="form.email" type="email" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="guide@treksphere.com" required />
                </div>
                <div class="col-md-6" v-if="!isEdit">
                  <label class="form-label text-secondary small">Password *</label>
                  <input v-model="form.password" type="password" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="Minimum 8 characters" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label text-secondary small">Contact Phone</label>
                  <input v-model="form.contact" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="e.g. 9876543210" />
                </div>
                <div class="col-md-6">
                  <label class="form-label text-secondary small">Experience (Years)</label>
                  <input v-model.number="form.experience_years" type="number" min="0" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="0" />
                </div>
                <div class="col-md-6" v-if="isEdit">
                  <label class="form-label text-secondary small">Account Status</label>
                  <select v-model="form.is_active" class="form-select bg-black bg-opacity-25 border-secondary text-light">
                    <option :value="true">Active / Unlocked</option>
                    <option :value="false">Blocked / Deactivated</option>
                  </select>
                </div>
                <div class="col-12">
                  <label class="form-label text-secondary small">Skills (Comma-separated)</label>
                  <input v-model="form.skills" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="e.g. First Aid, Mountain Navigation, Rock Climbing" />
                </div>
                <div class="col-12">
                  <label class="form-label text-secondary small">Short Bio</label>
                  <textarea v-model="form.bio" class="form-control bg-black bg-opacity-25 border-secondary text-light" rows="3" placeholder="Describe the guide's background, certifications, and specialties..."></textarea>
                </div>
              </div>
            </div>
            <div class="modal-footer border-secondary border-opacity-25">
              <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="submit" class="btn btn-glow px-4" :disabled="submitting">
                <span v-if="submitting" class="spinner-border spinner-border-sm me-1" role="status"></span>
                {{ isEdit ? 'Save Changes' : 'Register Leader' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    </Teleport>
  </DashboardLayout>
</template>

<script>
import { adminService } from '../../services/api';
import { alertService } from '@/services/alert';
import { confirmService } from '@/services/confirm';
import DashboardLayout from '../../components/DashboardLayout.vue';
import { Modal } from 'bootstrap';

export default {
  name: 'AdminStaff',
  components: {
    DashboardLayout
  },
  data() {
    return {
      staffList: [],
      loading: true,
      submitting: false,
      isEdit: false,
      currentStaffId: null,
      filters: {
        search: ''
      },
      form: {
        name: '',
        email: '',
        password: '',
        contact: '',
        experience_years: 0,
        skills: '',
        bio: '',
        is_active: true
      },
      modalInstance: null
    };
  },
  methods: {
    async fetchStaff() {
      this.loading = true;
      try {
        const data = await adminService.getStaff({ search: this.filters.search });
        this.staffList = data;
      } catch (err) {
        console.error('Failed to load staff list', err);
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.form = {
        name: '',
        email: '',
        password: '',
        contact: '',
        experience_years: 0,
        skills: '',
        bio: '',
        is_active: true
      };
    },
    openCreateModal() {
      this.isEdit = false;
      this.resetForm();
      this.modalInstance.show();
    },
    openEditModal(staff) {
      this.isEdit = true;
      this.currentStaffId = staff.id;
      this.form = {
        name: staff.name,
        email: staff.email,
        password: '',
        contact: staff.contact,
        experience_years: staff.experience_years,
        skills: staff.skills,
        bio: staff.bio,
        is_active: staff.is_active
      };
      this.modalInstance.show();
    },
    async saveStaff() {
      this.submitting = true;
      try {
        if (this.isEdit) {
          await adminService.updateStaff(this.currentStaffId, this.form);
          alertService.success('Staff profile updated successfully!');
        } else {
          await adminService.createStaff(this.form);
          alertService.success('Staff member registered successfully!');
        }
        this.modalInstance.hide();
        this.fetchStaff();
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Error occurred while saving staff details.');
      } finally {
        this.submitting = false;
      }
    },
    async toggleActiveStatus(staff) {
      const confirmMsg = staff.is_active 
        ? `Are you sure you want to deactivate/blacklist guide "${staff.name}"?\nThey will be blocked from logging in immediately.`
        : `Unlock and activate guide "${staff.name}"?`;
      
      const confirmed = await confirmService.ask(confirmMsg, {
        title: staff.is_active ? 'Deactivate Guide' : 'Activate Guide',
        isDanger: staff.is_active
      });
      
      if (confirmed) {
        try {
          await adminService.toggleStaffStatus(staff.id, !staff.is_active);
          alertService.success('Status updated successfully!');
          this.fetchStaff();
        } catch (err) {
          alertService.error('Failed to update status.');
        }
      }
    }
  },
  mounted() {
    this.fetchStaff();
    
    // Initialize bootstrap modal safely after DOM is ready
    this.$nextTick(() => {
      const modalEl = this.$refs.staffModal;
      if (modalEl) {
        this.modalInstance = new Modal(modalEl);
      }
      // If query string has create=true, open modal immediately
      if (this.$route.query.create === 'true') {
        this.openCreateModal();
      }
    });
  }
}
</script>

<style scoped>
.hover-card {
  transition: transform 0.3s ease, border-color 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 242, 254, 0.4) !important;
}

.text-line-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
