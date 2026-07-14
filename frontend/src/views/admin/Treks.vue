<template>
  <DashboardLayout role="admin">
    <!-- Header & Create Trigger -->
    <div class="row align-items-center mb-5">
      <div class="col-md-6 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Manage <span class="text-gradient">Treks</span></h1>
        <p class="text-secondary mb-0">Create, edit, delete, or assign staff to treks</p>
      </div>
      <div class="col-md-6 text-center text-md-end mt-3 mt-md-0">
        <button @click="openCreateModal" class="btn btn-glow px-4 py-2">
          <i class="bi bi-plus-circle-fill me-2"></i>Create New Trek
        </button>
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 mb-4 shadow">
      <div class="row g-3">
        <div class="col-md-6">
          <div class="input-group">
            <span class="input-group-text bg-black bg-opacity-25 border-secondary text-secondary"><i class="bi bi-search"></i></span>
            <input 
              v-model="filters.search" 
              @input="fetchTreks" 
              type="text" 
              class="form-control bg-black bg-opacity-25 border-secondary text-light" 
              placeholder="Search by trek name or ID..."
            />
          </div>
        </div>
        <div class="col-6 col-md-3">
          <select v-model="filters.difficulty" @change="fetchTreks" class="form-select bg-black bg-opacity-25 border-secondary text-light">
            <option value="">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
            <option value="Expert">Expert</option>
          </select>
        </div>
        <div class="col-6 col-md-3">
          <select v-model="filters.status" @change="fetchTreks" class="form-select bg-black bg-opacity-25 border-secondary text-light">
            <option value="">All Statuses</option>
            <option value="Pending">Pending</option>
            <option value="Open">Open</option>
            <option value="Active">Active</option>
            <option value="Completed">Completed</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Treks Grid / List -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-info" role="status"></div>
    </div>

    <div v-else-if="treks.length === 0" class="card bg-dark bg-opacity-25 border-secondary border-opacity-10 text-center py-5">
      <span class="display-3 mb-2 d-block text-secondary"><i class="bi bi-compass"></i></span>
      <p class="text-secondary mb-0">No treks found in database.</p>
    </div>

    <div v-else class="row g-4">
      <div class="col-md-6 col-lg-4" v-for="trek in treks" :key="trek.id">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow h-100 rounded-4 overflow-hidden position-relative hover-card">
          <!-- Difficulty Badge -->
          <div class="position-absolute top-0 end-0 m-3 z-1">
            <span class="badge rounded-pill px-3 py-1 bg-black bg-opacity-60 border border-opacity-20 text-light" :class="getDifficultyClass(trek.difficulty)">
              {{ trek.difficulty }}
            </span>
          </div>

          <div class="p-4 d-flex flex-column h-100">
            <div class="mb-3">
              <span class="text-info small fw-bold">ID: {{ trek.id }}</span>
              <h5 class="fw-bold text-light mb-1 mt-1">{{ trek.name }}</h5>
              <div class="text-secondary small d-flex align-items-center gap-1">
                <i class="bi bi-geo-alt-fill text-danger"></i> {{ trek.location }}
              </div>
            </div>

            <p class="text-secondary small mb-4 flex-grow-1 text-line-clamp">
              {{ trek.description || 'No description provided for this trek.' }}
            </p>

            <div class="p-3 bg-black bg-opacity-25 rounded-3 mb-4 border border-secondary border-opacity-10">
              <div class="row g-2 text-center">
                <div class="col-4 border-end border-secondary border-opacity-25">
                  <span class="text-secondary tiny-text d-block">Duration</span>
                  <strong class="text-light text-nowrap">{{ trek.duration }} Days</strong>
                </div>
                <div class="col-4 border-end border-secondary border-opacity-25">
                  <span class="text-secondary tiny-text d-block">Booked Slots</span>
                  <strong class="text-light">{{ trek.current_participants }} / {{ trek.max_slots }}</strong>
                </div>
                <div class="col-4">
                  <span class="text-secondary tiny-text d-block">Guide</span>
                  <strong class="text-warning text-truncate d-block small" :title="trek.assigned_staff_name">
                    {{ trek.assigned_staff_name }}
                  </strong>
                </div>
              </div>
            </div>

            <div class="d-flex justify-content-between align-items-center mt-auto border-top border-secondary border-opacity-10 pt-3">
              <span class="badge" :class="getStatusClass(trek.status)">{{ trek.status }}</span>
              <div class="d-flex gap-2">
                <button @click="openEditModal(trek)" class="btn btn-outline-info btn-sm rounded-3" title="Edit Trek">
                  <i class="bi bi-pencil-square"></i>
                </button>
                <button @click="confirmDelete(trek)" class="btn btn-outline-danger btn-sm rounded-3" title="Delete Trek">
                  <i class="bi bi-trash-fill"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bootstrap Modal for Create/Edit (Teleported to body to avoid stacking context issues) -->
    <Teleport to="body">
    <div class="modal fade" id="trekModal" tabindex="-1" aria-hidden="true" ref="trekModal">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content bg-dark text-light border border-secondary border-opacity-50 rounded-4">
          <div class="modal-header border-secondary border-opacity-25">
            <h5 class="modal-title fw-bold text-light">
              {{ isEdit ? 'Edit Trek' : 'Create Trek' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="saveTrek">
            <div class="modal-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label text-secondary small">Trek Name *</label>
                  <input v-model="form.name" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="e.g. Kedarnath Trek" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label text-secondary small">Location *</label>
                  <input v-model="form.location" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="e.g. Uttarakhand, India" required />
                </div>
                <div class="col-md-4">
                  <label class="form-label text-secondary small">Difficulty *</label>
                  <select v-model="form.difficulty" class="form-select bg-black bg-opacity-25 border-secondary text-light" required>
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                    <option value="Expert">Expert</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label text-secondary small">Max slots *</label>
                  <input v-model.number="form.max_slots" type="number" min="1" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="e.g. 20" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label text-secondary small">Start Date *</label>
                  <input v-model="form.start_date" type="date" class="form-control bg-black bg-opacity-25 border-secondary text-light" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label text-secondary small">End Date *</label>
                  <input v-model="form.end_date" type="date" class="form-control bg-black bg-opacity-25 border-secondary text-light" :min="form.start_date" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label text-secondary small">Assign Staff Guide</label>
                  <select v-model="form.assigned_staff_id" class="form-select bg-black bg-opacity-25 border-secondary text-light">
                    <option :value="null">Unassigned</option>
                    <option v-for="staff in staffOptions" :key="staff.id" :value="staff.id">
                      {{ staff.name }} ({{ staff.experience_years }} yrs exp)
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label text-secondary small">Status *</label>
                  <select v-model="form.status" class="form-select bg-black bg-opacity-25 border-secondary text-light" required>
                    <option value="Pending">Pending</option>
                    <option value="Open">Open</option>
                    <option value="Active">Active</option>
                    <option value="Completed">Completed</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
                <div class="col-12">
                  <label class="form-label text-secondary small">Description</label>
                  <textarea v-model="form.description" class="form-control bg-black bg-opacity-25 border-secondary text-light" rows="3" placeholder="Describe the trek, highlights, terrain, and what participants can expect..."></textarea>
                </div>
              </div>
            </div>
            <div class="modal-footer border-secondary border-opacity-25">
              <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="submit" class="btn btn-glow px-4" :disabled="submitting">
                <span v-if="submitting" class="spinner-border spinner-border-sm me-1" role="status"></span>
                {{ isEdit ? 'Save Changes' : 'Create Trek' }}
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
import DashboardLayout from '../../components/DashboardLayout.vue';
import { Modal } from 'bootstrap';

export default {
  name: 'AdminTreks',
  components: {
    DashboardLayout
  },
  data() {
    return {
      treks: [],
      staffOptions: [],
      loading: true,
      submitting: false,
      isEdit: false,
      currentTrekId: null,
      filters: {
        search: '',
        difficulty: '',
        status: ''
      },
      form: {
        name: '',
        description: '',
        location: '',
        difficulty: 'Medium',
        duration: 3,
        max_slots: 15,
        start_date: '',
        end_date: '',
        assigned_staff_id: null,
        status: 'Open'
      },
      modalInstance: null
    };
  },
  computed: {
    calculatedDuration() {
      if (!this.form.start_date || !this.form.end_date) return 0;
      const start = new Date(this.form.start_date);
      const end = new Date(this.form.end_date);
      if (isNaN(start) || isNaN(end) || end < start) return 0;
      // +1 so a single-day trek counts as 1 day
      return Math.round((end - start) / (1000 * 60 * 60 * 24)) + 1;
    }
  },
  watch: {
    calculatedDuration(val) {
      this.form.duration = val > 0 ? val : this.form.duration;
    },
    'form.start_date'(newVal) {
      // If end date is before new start date, reset end date
      if (this.form.end_date && this.form.end_date < newVal) {
        this.form.end_date = '';
      }
    }
  },
  methods: {
    async fetchTreks() {
      this.loading = true;
      try {
        const data = await adminService.getTreks({
          search: this.filters.search,
          difficulty: this.filters.difficulty,
          status: this.filters.status
        });
        this.treks = data;
      } catch (err) {
        console.error('Failed to load treks', err);
      } finally {
        this.loading = false;
      }
    },
    async fetchStaffOptions() {
      try {
        const staff = await adminService.getStaff();
        this.staffOptions = staff.filter(s => s.is_active);
      } catch (err) {
        console.error('Failed to load staff options', err);
      }
    },
    resetForm() {
      this.form = {
        name: '',
        description: '',
        location: '',
        difficulty: 'Medium',
        duration: 3,
        max_slots: 15,
        start_date: '',
        end_date: '',
        assigned_staff_id: null,
        status: 'Open'
      };
    },
    openCreateModal() {
      this.isEdit = false;
      this.resetForm();
      this.modalInstance.show();
    },
    openEditModal(trek) {
      this.isEdit = true;
      this.currentTrekId = trek.id;
      this.form = {
        name: trek.name,
        description: trek.description,
        location: trek.location,
        difficulty: trek.difficulty,
        duration: trek.duration,
        max_slots: trek.max_slots,
        start_date: trek.start_date,
        end_date: trek.end_date,
        assigned_staff_id: trek.assigned_staff_id,
        status: trek.status
      };
      this.modalInstance.show();
    },
    async saveTrek() {
      this.submitting = true;
      try {
        if (this.isEdit) {
          await adminService.updateTrek(this.currentTrekId, this.form);
          alert('Trek updated successfully!');
        } else {
          await adminService.createTrek(this.form);
          alert('Trek created successfully!');
        }
        this.modalInstance.hide();
        this.fetchTreks();
      } catch (err) {
        alert(err.response?.data?.message || 'Error occurred while saving.');
      } finally {
        this.submitting = false;
      }
    },
    async confirmDelete(trek) {
      if (confirm(`Are you sure you want to permanently delete the trek "${trek.name}"?\nWarning: This will also cancel all associated bookings!`)) {
        try {
          await adminService.deleteTrek(trek.id);
          alert('Trek deleted successfully!');
          this.fetchTreks();
        } catch (err) {
          alert('Failed to delete trek.');
        }
      }
    },
    getDifficultyClass(diff) {
      switch (diff) {
        case 'Easy': return 'border-success text-success';
        case 'Medium': return 'border-primary text-primary';
        case 'Hard': return 'border-warning text-warning';
        case 'Expert': return 'border-danger text-danger';
        default: return 'border-secondary text-secondary';
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 'Open': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Active': return 'bg-info bg-opacity-25 text-info border border-info border-opacity-25';
        case 'Pending': return 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        case 'Completed': return 'bg-secondary bg-opacity-25 text-secondary border border-secondary border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    }
  },
  mounted() {
    this.fetchTreks();
    this.fetchStaffOptions();
    
    // Initialize bootstrap modal safely after DOM is ready
    this.$nextTick(() => {
      const modalEl = this.$refs.trekModal;
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
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
