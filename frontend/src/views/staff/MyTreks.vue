<template>
  <DashboardLayout role="staff">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">My <span class="text-gradient">Assigned Treks</span></h1>
        <p class="text-secondary mb-0">Track and manage operations for trekking routes assigned to you.</p>
      </div>
    </div>

    <!-- Assigned Treks List -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-info" role="status"></div>
    </div>

    <div v-else-if="treks.length === 0" class="card bg-dark bg-opacity-25 border-secondary border-opacity-10 text-center py-5 rounded-4 p-4">
      <span class="display-3 mb-2 d-block text-secondary"><i class="bi bi-compass-refraction"></i></span>
      <p class="text-secondary mb-0">No treks assigned to you yet.</p>
    </div>

    <div v-else class="d-flex flex-column gap-5">
      
      <!-- 1. ACTIVE / ONGOING SECTION -->
      <div v-if="activeTreks.length > 0" class="section-group">
        <h4 class="h5 fw-bold text-gradient-info mb-4 d-flex align-items-center gap-2">
          <span class="status-dot bg-info"></span>
          Active / Ongoing Expeditions ({{ activeTreks.length }})
        </h4>
        <div class="row g-4">
          <div class="col-md-6 col-xl-4" v-for="trek in activeTreks" :key="trek.id">
            <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100 position-relative hover-card">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="text-info small fw-bold">ID: #{{ trek.id }}</span>
                <span class="badge rounded-pill px-3 py-1" :class="getStatusClass(trek.status)">{{ trek.status }}</span>
              </div>

              <h5 class="fw-bold text-light mb-1 mt-1">{{ trek.name }}</h5>
              <div class="text-secondary small mb-3"><i class="bi bi-geo-alt me-1"></i> {{ trek.location }}</div>

              <div class="p-3 bg-black bg-opacity-25 rounded-3 mb-4 border border-secondary border-opacity-10">
                <div class="row g-2 text-center">
                  <div class="col-6 border-end border-secondary border-opacity-25">
                    <span class="text-secondary tiny-text d-block">Duration</span>
                    <strong class="text-light text-nowrap small">{{ trek.duration }} Days</strong>
                  </div>
                  <div class="col-6">
                    <span class="text-secondary tiny-text d-block">Booked Slots</span>
                    <strong class="text-light small">{{ trek.current_participants }} / {{ trek.max_slots }}</strong>
                  </div>
                </div>
              </div>

              <div class="d-flex flex-column gap-2 mt-auto pt-3 border-top border-secondary border-opacity-10">
                <div class="d-flex flex-column gap-1 mb-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="small text-secondary">Start: {{ formatDate(trek.start_date) }}</span>
                    <span class="small text-secondary">End: {{ formatDate(trek.end_date) }}</span>
                  </div>
                  <span class="small text-secondary mt-1" v-if="trek.last_booking_time" style="font-size: 0.75rem;">
                    <i class="bi bi-clock-history me-1"></i> Last Booking: {{ formatDateTime(trek.last_booking_time) }}
                  </span>
                  <span class="small text-secondary mt-1" style="font-size: 0.75rem; display: block;">
                    <i class="bi bi-calendar-x me-1"></i> Bookings: 
                    <span :class="trek.booking_closed ? 'text-danger fw-bold' : 'text-light'">
                      <span v-if="trek.booking_closed">Closed</span>
                      <span v-else-if="trek.booking_close_time">{{ formatDateTime(trek.booking_close_time) }}</span>
                      <span v-else>Open</span>
                    </span>
                  </span>
                </div>

                <!-- Operations Section -->
                <div class="mt-2 d-flex flex-column gap-2 w-100">
                  <div class="d-flex gap-2">
                    <div class="flex-grow-1">
                      <select :value="trek.status" @change="updateStatus(trek.id, $event.target.value)" class="form-select form-select-sm bg-dark text-light border-secondary py-2 rounded-3 w-100">
                        <option value="Pending">Pending</option>
                        <option value="Open">Open</option>
                        <option value="Active">Active (Ongoing)</option>
                        <option value="Completed">Completed</option>
                        <option value="Cancelled">Cancelled</option>
                      </select>
                    </div>
                    <div>
                      <button @click="openSlotsModal(trek)" class="btn btn-outline-info btn-sm py-2 rounded-3 px-3">
                        <i class="bi bi-pencil-square"></i> Slots
                      </button>
                    </div>
                  </div>

                  <!-- Shortcuts -->
                  <div class="d-grid mt-1">
                    <button v-if="!trek.booking_closed && trek.status === 'Open'" @click="closeBooking(trek)" class="btn btn-outline-warning btn-sm rounded-3 py-2 fw-bold mb-2">
                      <i class="bi bi-calendar-x me-1"></i>Close Booking
                    </button>
                    <button v-if="trek.status === 'Open' || trek.status === 'Pending'" @click="updateStatus(trek.id, 'Active')" class="btn btn-outline-info btn-sm rounded-3 py-2 fw-bold">
                      <i class="bi bi-play-fill me-1"></i>Start Trek
                    </button>
                    <button v-if="trek.status === 'Active'" @click="updateStatus(trek.id, 'Completed')" class="btn btn-outline-success btn-sm rounded-3 py-2 fw-bold">
                      <i class="bi bi-check-lg me-1"></i>Complete Trek
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. OPEN FOR BOOKINGS SECTION -->
      <div v-if="openTreks.length > 0" class="section-group">
        <h4 class="h5 fw-bold text-gradient-success mb-4 d-flex align-items-center gap-2">
          <span class="status-dot bg-success"></span>
          Open for Bookings ({{ openTreks.length }})
        </h4>
        <div class="row g-4">
          <div class="col-md-6 col-xl-4" v-for="trek in openTreks" :key="trek.id">
            <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100 position-relative hover-card">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="text-info small fw-bold">ID: #{{ trek.id }}</span>
                <span class="badge rounded-pill px-3 py-1" :class="getStatusClass(trek.status)">{{ trek.status }}</span>
              </div>

              <h5 class="fw-bold text-light mb-1 mt-1">{{ trek.name }}</h5>
              <div class="text-secondary small mb-3"><i class="bi bi-geo-alt me-1"></i> {{ trek.location }}</div>

              <div class="p-3 bg-black bg-opacity-25 rounded-3 mb-4 border border-secondary border-opacity-10">
                <div class="row g-2 text-center">
                  <div class="col-6 border-end border-secondary border-opacity-25">
                    <span class="text-secondary tiny-text d-block">Duration</span>
                    <strong class="text-light text-nowrap small">{{ trek.duration }} Days</strong>
                  </div>
                  <div class="col-6">
                    <span class="text-secondary tiny-text d-block">Booked Slots</span>
                    <strong class="text-light small">{{ trek.current_participants }} / {{ trek.max_slots }}</strong>
                  </div>
                </div>
              </div>

              <div class="d-flex flex-column gap-2 mt-auto pt-3 border-top border-secondary border-opacity-10">
                <div class="d-flex flex-column gap-1 mb-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="small text-secondary">Start: {{ formatDate(trek.start_date) }}</span>
                    <span class="small text-secondary">End: {{ formatDate(trek.end_date) }}</span>
                  </div>
                  <span class="small text-secondary mt-1" v-if="trek.last_booking_time" style="font-size: 0.75rem;">
                    <i class="bi bi-clock-history me-1"></i> Last Booking: {{ formatDateTime(trek.last_booking_time) }}
                  </span>
                  <span class="small text-secondary mt-1" style="font-size: 0.75rem; display: block;">
                    <i class="bi bi-calendar-x me-1"></i> Bookings: 
                    <span :class="trek.booking_closed ? 'text-danger fw-bold' : 'text-light'">
                      <span v-if="trek.booking_closed">Closed</span>
                      <span v-else-if="trek.booking_close_time">{{ formatDateTime(trek.booking_close_time) }}</span>
                      <span v-else>Open</span>
                    </span>
                  </span>
                </div>

                <!-- Operations Section -->
                <div class="mt-2 d-flex flex-column gap-2 w-100">
                  <div class="d-flex gap-2">
                    <div class="flex-grow-1">
                      <select :value="trek.status" @change="updateStatus(trek.id, $event.target.value)" class="form-select form-select-sm bg-dark text-light border-secondary py-2 rounded-3 w-100">
                        <option value="Pending">Pending</option>
                        <option value="Open">Open</option>
                        <option value="Active">Active (Ongoing)</option>
                        <option value="Completed">Completed</option>
                        <option value="Cancelled">Cancelled</option>
                      </select>
                    </div>
                    <div>
                      <button @click="openSlotsModal(trek)" class="btn btn-outline-info btn-sm py-2 rounded-3 px-3">
                        <i class="bi bi-pencil-square"></i> Slots
                      </button>
                    </div>
                  </div>

                  <!-- Shortcuts -->
                  <div class="d-grid mt-1">
                    <button v-if="!trek.booking_closed && trek.status === 'Open'" @click="closeBooking(trek)" class="btn btn-outline-warning btn-sm rounded-3 py-2 fw-bold mb-2">
                      <i class="bi bi-calendar-x me-1"></i>Close Booking
                    </button>
                    <button v-if="trek.status === 'Open' || trek.status === 'Pending'" @click="updateStatus(trek.id, 'Active')" class="btn btn-outline-info btn-sm rounded-3 py-2 fw-bold">
                      <i class="bi bi-play-fill me-1"></i>Start Trek
                    </button>
                    <button v-if="trek.status === 'Active'" @click="updateStatus(trek.id, 'Completed')" class="btn btn-outline-success btn-sm rounded-3 py-2 fw-bold">
                      <i class="bi bi-check-lg me-1"></i>Complete Trek
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. PENDING / CLOSED SECTION -->
      <div v-if="pendingTreks.length > 0" class="section-group">
        <h4 class="h5 fw-bold text-gradient-warning mb-4 d-flex align-items-center gap-2">
          <span class="status-dot bg-warning"></span>
          Pending / Closed ({{ pendingTreks.length }})
        </h4>
        <div class="row g-4">
          <div class="col-md-6 col-xl-4" v-for="trek in pendingTreks" :key="trek.id">
            <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100 position-relative hover-card">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="text-info small fw-bold">ID: #{{ trek.id }}</span>
                <span class="badge rounded-pill px-3 py-1" :class="getStatusClass(trek.status)">{{ trek.status }}</span>
              </div>

              <h5 class="fw-bold text-light mb-1 mt-1">{{ trek.name }}</h5>
              <div class="text-secondary small mb-3"><i class="bi bi-geo-alt me-1"></i> {{ trek.location }}</div>

              <div class="p-3 bg-black bg-opacity-25 rounded-3 mb-4 border border-secondary border-opacity-10">
                <div class="row g-2 text-center">
                  <div class="col-6 border-end border-secondary border-opacity-25">
                    <span class="text-secondary tiny-text d-block">Duration</span>
                    <strong class="text-light text-nowrap small">{{ trek.duration }} Days</strong>
                  </div>
                  <div class="col-6">
                    <span class="text-secondary tiny-text d-block">Booked Slots</span>
                    <strong class="text-light small">{{ trek.current_participants }} / {{ trek.max_slots }}</strong>
                  </div>
                </div>
              </div>

              <div class="d-flex flex-column gap-2 mt-auto pt-3 border-top border-secondary border-opacity-10">
                <div class="d-flex flex-column gap-1 mb-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="small text-secondary">Start: {{ formatDate(trek.start_date) }}</span>
                    <span class="small text-secondary">End: {{ formatDate(trek.end_date) }}</span>
                  </div>
                  <span class="small text-secondary mt-1" v-if="trek.last_booking_time" style="font-size: 0.75rem;">
                    <i class="bi bi-clock-history me-1"></i> Last Booking: {{ formatDateTime(trek.last_booking_time) }}
                  </span>
                  <span class="small text-secondary mt-1" style="font-size: 0.75rem; display: block;">
                    <i class="bi bi-calendar-x me-1"></i> Bookings: 
                    <span :class="trek.booking_closed ? 'text-danger fw-bold' : 'text-light'">
                      <span v-if="trek.booking_closed">Closed</span>
                      <span v-else-if="trek.booking_close_time">{{ formatDateTime(trek.booking_close_time) }}</span>
                      <span v-else>Open</span>
                    </span>
                  </span>
                </div>

                <!-- Operations Section -->
                <div class="mt-2 d-flex flex-column gap-2 w-100">
                  <div class="d-flex gap-2">
                    <div class="flex-grow-1">
                      <select :value="trek.status" @change="updateStatus(trek.id, $event.target.value)" class="form-select form-select-sm bg-dark text-light border-secondary py-2 rounded-3 w-100">
                        <option value="Pending">Pending</option>
                        <option value="Open">Open</option>
                        <option value="Active">Active (Ongoing)</option>
                        <option value="Completed">Completed</option>
                        <option value="Cancelled">Cancelled</option>
                      </select>
                    </div>
                    <div>
                      <button @click="openSlotsModal(trek)" class="btn btn-outline-info btn-sm py-2 rounded-3 px-3">
                        <i class="bi bi-pencil-square"></i> Slots
                      </button>
                    </div>
                  </div>

                  <!-- Shortcuts -->
                  <div class="d-grid mt-1">
                    <button v-if="!trek.booking_closed && trek.status === 'Open'" @click="closeBooking(trek)" class="btn btn-outline-warning btn-sm rounded-3 py-2 fw-bold mb-2">
                      <i class="bi bi-calendar-x me-1"></i>Close Booking
                    </button>
                    <button v-if="trek.status === 'Open' || trek.status === 'Pending'" @click="updateStatus(trek.id, 'Active')" class="btn btn-outline-info btn-sm rounded-3 py-2 fw-bold">
                      <i class="bi bi-play-fill me-1"></i>Start Trek
                    </button>
                    <button v-if="trek.status === 'Active'" @click="updateStatus(trek.id, 'Completed')" class="btn btn-outline-success btn-sm rounded-3 py-2 fw-bold">
                      <i class="bi bi-check-lg me-1"></i>Complete Trek
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. COMPLETED & CANCELLED SECTION -->
      <div v-if="completedCancelledTreks.length > 0" class="section-group">
        <h4 class="h5 fw-bold text-gradient-secondary mb-4 d-flex align-items-center gap-2">
          <span class="status-dot bg-secondary"></span>
          Completed & Cancelled ({{ completedCancelledTreks.length }})
        </h4>
        <div class="row g-4">
          <div class="col-md-6 col-xl-4" v-for="trek in completedCancelledTreks" :key="trek.id">
            <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100 position-relative hover-card">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="text-info small fw-bold">ID: #{{ trek.id }}</span>
                <span class="badge rounded-pill px-3 py-1" :class="getStatusClass(trek.status)">{{ trek.status }}</span>
              </div>

              <h5 class="fw-bold text-light mb-1 mt-1">{{ trek.name }}</h5>
              <div class="text-secondary small mb-3"><i class="bi bi-geo-alt me-1"></i> {{ trek.location }}</div>

              <div class="p-3 bg-black bg-opacity-25 rounded-3 mb-4 border border-secondary border-opacity-10">
                <div class="row g-2 text-center">
                  <div class="col-6 border-end border-secondary border-opacity-25">
                    <span class="text-secondary tiny-text d-block">Duration</span>
                    <strong class="text-light text-nowrap small">{{ trek.duration }} Days</strong>
                  </div>
                  <div class="col-6">
                    <span class="text-secondary tiny-text d-block">Booked Slots</span>
                    <strong class="text-light small">{{ trek.current_participants }} / {{ trek.max_slots }}</strong>
                  </div>
                </div>
              </div>

              <div class="d-flex flex-column gap-2 mt-auto pt-3 border-top border-secondary border-opacity-10">
                <div class="d-flex flex-column gap-1 mb-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="small text-secondary">Start: {{ formatDate(trek.start_date) }}</span>
                    <span class="small text-secondary">End: {{ formatDate(trek.end_date) }}</span>
                  </div>
                  <span class="small text-secondary mt-1" v-if="trek.last_booking_time" style="font-size: 0.75rem;">
                    <i class="bi bi-clock-history me-1"></i> Last Booking: {{ formatDateTime(trek.last_booking_time) }}
                  </span>
                  <span class="small text-secondary mt-1" style="font-size: 0.75rem; display: block;">
                    <i class="bi bi-calendar-x me-1"></i> Bookings: 
                    <span :class="trek.booking_closed ? 'text-danger fw-bold' : 'text-light'">
                      <span v-if="trek.booking_closed">Closed</span>
                      <span v-else-if="trek.booking_close_time">{{ formatDateTime(trek.booking_close_time) }}</span>
                      <span v-else>Open</span>
                    </span>
                  </span>
                </div>

                <!-- Operations Section -->
                <div class="mt-2 d-flex flex-column gap-2 w-100">
                  <div class="d-flex gap-2">
                    <div class="flex-grow-1">
                      <select :value="trek.status" @change="updateStatus(trek.id, $event.target.value)" class="form-select form-select-sm bg-dark text-light border-secondary py-2 rounded-3 w-100">
                        <option value="Pending">Pending</option>
                        <option value="Open">Open</option>
                        <option value="Active">Active (Ongoing)</option>
                        <option value="Completed">Completed</option>
                        <option value="Cancelled">Cancelled</option>
                      </select>
                    </div>
                    <div>
                      <button @click="openSlotsModal(trek)" class="btn btn-outline-info btn-sm py-2 rounded-3 px-3">
                        <i class="bi bi-pencil-square"></i> Slots
                      </button>
                    </div>
                  </div>

                  <!-- Shortcuts -->
                  <div class="d-grid mt-1">
                    <button v-if="trek.status === 'Open' || trek.status === 'Pending'" @click="updateStatus(trek.id, 'Active')" class="btn btn-outline-info btn-sm rounded-3 py-2 fw-bold">
                      <i class="bi bi-play-fill me-1"></i>Start Trek
                    </button>
                    <button v-if="trek.status === 'Active'" @click="updateStatus(trek.id, 'Completed')" class="btn btn-outline-success btn-sm rounded-3 py-2 fw-bold">
                      <i class="bi bi-check-lg me-1"></i>Complete Trek
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Edit Slots Modal (Teleported to body) -->
    <Teleport to="body">
      <div v-if="slotsModalTrek" class="slots-backdrop" @click.self="closeSlotsModal">
        <div class="slots-sheet bg-dark text-light border border-secondary border-opacity-50 rounded-4 p-4">
          <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom border-secondary border-opacity-25">
            <h5 class="fw-bold mb-0 text-light">Update Trek Slots</h5>
            <button @click="closeSlotsModal" class="btn-close btn-close-white"></button>
          </div>

          <div class="mb-3">
            <p class="text-secondary small mb-1">Trek Name</p>
            <h6 class="text-light fw-bold">{{ slotsModalTrek.name }}</h6>
          </div>

          <div class="row g-2 mb-4 text-center">
            <div class="col-6 bg-black bg-opacity-20 border border-secondary border-opacity-10 rounded-3 py-2">
              <span class="text-secondary tiny-text d-block">Current Participants</span>
              <strong class="text-info fs-5">{{ slotsModalTrek.current_participants }}</strong>
            </div>
            <div class="col-6 bg-black bg-opacity-20 border border-secondary border-opacity-10 rounded-3 py-2">
              <span class="text-secondary tiny-text d-block">Current Max Capacity</span>
              <strong class="text-light fs-5">{{ slotsModalTrek.max_slots }}</strong>
            </div>
          </div>

          <form @submit.prevent="saveSlots">
            <div class="mb-4">
              <label class="form-label text-secondary small">New Maximum Capacity *</label>
              <input v-model.number="slotsForm.max_slots" type="number" :min="slotsModalTrek.current_participants" class="form-control bg-black bg-opacity-25 border-secondary text-light py-2" placeholder="e.g. 25" required />
              <div class="form-text text-secondary mt-1" style="font-size: 0.75rem;">
                Cannot be lower than the current booked participants ({{ slotsModalTrek.current_participants }}).
              </div>
            </div>

            <div class="d-flex gap-2 justify-content-end">
              <button type="button" @click="closeSlotsModal" class="btn btn-outline-secondary px-3 py-2 rounded-3">Cancel</button>
              <button type="submit" class="btn btn-glow px-4 py-2 rounded-3" :disabled="submitting">
                <span v-if="submitting" class="spinner-border spinner-border-sm me-1" role="status"></span>
                Save Slots
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </DashboardLayout>
</template>

<script>
import { staffService } from '../../services/api';
import { alertService } from '@/services/alert';
import { confirmService } from '@/services/confirm';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'StaffTreks',
  components: {
    DashboardLayout
  },
  data() {
    return {
      treks: [],
      loading: true,
      submitting: false,
      slotsModalTrek: null,
      slotsForm: {
        max_slots: 0
      }
    };
  },
  computed: {
    activeTreks() {
      return this.treks.filter(t => t.status === 'Active');
    },
    openTreks() {
      return this.treks.filter(t => t.status === 'Open');
    },
    pendingTreks() {
      return this.treks.filter(t => t.status === 'Pending' || t.status === 'Closed');
    },
    completedCancelledTreks() {
      return this.treks.filter(t => t.status === 'Completed' || t.status === 'Cancelled');
    }
  },
  methods: {
    async fetchTreks() {
      this.loading = true;
      try {
        const data = await staffService.getDashboardSummary();
        this.treks = data.assigned_treks;
      } catch (err) {
        console.error('Failed to load assigned treks', err);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-GB', { timeZone: 'Asia/Kolkata' });
      } catch (e) { return dateStr; }
    },
    formatDateTime(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        const d = new Date(dateStr);
        return d.toLocaleString('en-GB', { 
          timeZone: 'Asia/Kolkata', 
          day: '2-digit',
          month: '2-digit', 
          year: 'numeric', 
          hour: '2-digit', 
          minute: '2-digit',
          hour12: true
        });
      } catch (e) { return dateStr; }
    },
    getStatusClass(status) {
      switch (status) {
        case 'Completed': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Active': return 'bg-info bg-opacity-25 text-info border border-info border-opacity-25';
        case 'Open': return 'bg-primary bg-opacity-25 text-primary border border-primary border-opacity-25';
        case 'Pending': return 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    },
    async updateStatus(trekId, newStatus) {
      try {
        await staffService.updateTrekStatus(trekId, newStatus);
        alertService.success('Trek status updated successfully!');
        this.fetchTreks();
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Failed to update status.');
      }
    },
    async closeBooking(trek) {
      const confirmed = await confirmService.ask(
        `Are you sure you want to close bookings manually for "${trek.name}"?`,
        { title: 'Close Bookings', confirmText: 'Close Bookings', isDanger: true }
      );
      if (confirmed) {
        try {
          await staffService.closeBooking(trek.id);
          alertService.success('Bookings closed successfully!');
          this.fetchTreks();
        } catch (err) {
          alertService.error(err.response?.data?.message || 'Failed to close bookings.');
        }
      }
    },
    openSlotsModal(trek) {
      this.slotsModalTrek = trek;
      this.slotsForm.max_slots = trek.max_slots;
    },
    closeSlotsModal() {
      this.slotsModalTrek = null;
    },
    async saveSlots() {
      this.submitting = true;
      try {
        await staffService.updateTrekSlots(this.slotsModalTrek.id, this.slotsForm.max_slots);
        alertService.success('Trek capacity slots updated successfully!');
        this.closeSlotsModal();
        this.fetchTreks();
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Failed to update capacity.');
      } finally {
        this.submitting = false;
      }
    }
  },
  mounted() {
    this.fetchTreks();
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

/* Modal overlay styling */
.slots-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1060;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.slots-sheet {
  width: 100%;
  max-width: 460px;
  animation: scaleIn 0.2s ease-out;
}

@keyframes scaleIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Section styling */
.text-gradient-info {
  background: linear-gradient(135deg, #00f2fe, #4facfe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-gradient-success {
  background: linear-gradient(135deg, #4ade80, #22c55e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-gradient-warning {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-gradient-secondary {
  background: linear-gradient(135deg, #cbd5e1, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.section-group {
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(100, 116, 139, 0.1);
}
.section-group:last-child {
  border-bottom: none;
}
</style>
