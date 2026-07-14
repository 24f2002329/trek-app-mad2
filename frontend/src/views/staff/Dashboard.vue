<template>
  <DashboardLayout role="staff">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Staff <span class="text-gradient">Operations Center</span></h1>
        <p class="text-secondary mb-0">View assigned trekking expeditions, update real-time trek statuses, and monitor registered participants.</p>
      </div>
    </div>

    <!-- Active Today Banner -->
    <div class="mb-5" v-if="summary.today_treks.length > 0">
      <h4 class="h5 fw-bold text-gradient mb-3">
        <i class="bi bi-lightning-charge-fill text-warning me-1"></i> Active Expeditions Today
      </h4>
      <div class="row g-3">
        <div class="col-md-6" v-for="t in summary.today_treks" :key="t.id">
          <div class="card bg-info bg-opacity-10 border-info border-opacity-25 rounded-4 p-3 d-flex flex-row justify-content-between align-items-center shadow-sm">
            <div>
              <strong class="text-light fs-5">{{ t.name }}</strong>
              <div class="small text-secondary mt-1"><i class="bi bi-geo-alt-fill text-info me-1"></i> {{ t.location }}</div>
            </div>
            <span class="badge bg-info bg-opacity-20 text-info border border-info border-opacity-25 px-3 py-1 rounded-pill">{{ t.status }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="row g-4 mb-5">
      <div class="col-md-6">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 d-flex flex-row align-items-center gap-3">
          <div class="stat-icon bg-info bg-opacity-10 text-info border border-info border-opacity-25 rounded-circle d-flex align-items-center justify-content-center">
            <i class="bi bi-compass fs-3"></i>
          </div>
          <div>
            <h6 class="text-secondary mb-1 uppercase-label tiny-text">Assigned Treks</h6>
            <h3 class="fw-bold text-light mb-0">{{ summary.assigned_treks.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 d-flex flex-row align-items-center gap-3">
          <div class="stat-icon bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 rounded-circle d-flex align-items-center justify-content-center">
            <i class="bi bi-people fs-3"></i>
          </div>
          <div>
            <h6 class="text-secondary mb-1 uppercase-label tiny-text">Total Trekkers</h6>
            <h3 class="fw-bold text-light mb-0">{{ summary.participants.length }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Details Columns -->
    <div class="row g-4">
      <!-- Assigned Treks list -->
      <div class="col-lg-7">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="h5 fw-bold mb-0 text-light">Assigned Expeditions</h4>
            <router-link to="/staff/treks" class="btn btn-outline-info btn-sm rounded-3 px-3">View All</router-link>
          </div>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <div v-else-if="summary.assigned_treks.length === 0" class="text-center py-5">
            <span class="display-4 d-block mb-3 text-secondary"><i class="bi bi-journal-x"></i></span>
            <p class="text-secondary mb-0">No treks assigned to you yet.</p>
          </div>

          <div v-else class="d-flex flex-column gap-3">
            <div v-for="trek in summary.assigned_treks" :key="trek.id" class="p-3 rounded-4 bg-black bg-opacity-20 border border-secondary border-opacity-15">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                  <h6 class="fw-bold text-light mb-1">{{ trek.name }}</h6>
                  <span class="small text-secondary d-block"><i class="bi bi-geo-alt me-1"></i> {{ trek.location }}</span>
                  <span class="small text-secondary d-block mt-1"><i class="bi bi-calendar-event me-1"></i> {{ formatDate(trek.start_date) }}</span>
                  <span class="small text-secondary d-block mt-1" v-if="trek.last_booking_time">
                    <i class="bi bi-clock-history me-1"></i> Last Booking: {{ formatDateTime(trek.last_booking_time) }}
                  </span>
                  <span class="small text-secondary d-block mt-1">
                    <i class="bi bi-calendar-x me-1"></i> Bookings: 
                    <span :class="trek.booking_closed ? 'text-danger fw-bold' : 'text-light'">
                      <span v-if="trek.booking_closed">Closed</span>
                      <span v-else-if="trek.booking_close_time">{{ formatDateTime(trek.booking_close_time) }}</span>
                      <span v-else>Open</span>
                    </span>
                  </span>
                </div>
                <span class="badge rounded-pill px-3 py-1" :class="getStatusClass(trek.status)">{{ trek.status }}</span>
              </div>
              
              <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3 pt-3 border-top border-secondary border-opacity-10">
                <div class="small text-secondary">
                  Slots Booked: <strong class="text-light">{{ trek.current_participants }} / {{ trek.max_slots }}</strong>
                </div>
                
                <div class="d-flex align-items-center gap-2">
                  <!-- Shortcuts -->
                  <button v-if="!trek.booking_closed && trek.status === 'Open'" @click="closeBooking(trek)" class="btn btn-outline-warning btn-sm rounded-3 py-1 px-3 fw-bold">
                    <i class="bi bi-calendar-x me-1"></i>Close Booking
                  </button>
                  <button v-if="trek.status === 'Open' || trek.status === 'Pending'" @click="updateStatus(trek.id, 'Active')" class="btn btn-outline-info btn-sm rounded-3 py-1 px-3 fw-bold">
                    <i class="bi bi-play-fill me-1"></i>Start Trek
                  </button>
                  <button v-if="trek.status === 'Active'" @click="updateStatus(trek.id, 'Completed')" class="btn btn-outline-success btn-sm rounded-3 py-1 px-3 fw-bold">
                    <i class="bi bi-check-lg me-1"></i>Complete Trek
                  </button>

                  <span class="small text-secondary text-nowrap ms-2">Status:</span>
                  <select :value="trek.status" @change="updateStatus(trek.id, $event.target.value)" class="form-select form-select-sm bg-dark text-light border-secondary py-1 px-2 rounded-3" style="width: auto;">
                    <option value="Pending">Pending</option>
                    <option value="Open">Open</option>
                    <option value="Active">Active</option>
                    <option value="Completed">Completed</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Trekkers list -->
      <div class="col-lg-5">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="h5 fw-bold mb-0 text-light">Recent Registrations</h4>
            <router-link to="/staff/participants" class="btn btn-outline-info btn-sm rounded-3 px-3">Participants</router-link>
          </div>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <div v-else-if="summary.participants.length === 0" class="text-center py-5">
            <span class="display-4 d-block mb-3 text-secondary"><i class="bi bi-people"></i></span>
            <p class="text-secondary mb-0">No participants registered yet.</p>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
              <thead>
                <tr>
                  <th class="text-secondary border-secondary small">Name</th>
                  <th class="text-secondary border-secondary small">Trek</th>
                  <th class="text-secondary border-secondary text-center small">Slots</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(p, idx) in summary.participants.slice(0, 5)" :key="idx">
                  <td class="border-secondary border-opacity-10">
                    <div class="fw-bold text-light text-truncate small" style="max-width: 110px;">{{ p.trekker_name }}</div>
                    <span class="text-secondary small d-block text-truncate" style="max-width: 110px;">{{ p.email }}</span>
                  </td>
                  <td class="border-secondary border-opacity-10 text-light small">
                    <span class="text-truncate d-block text-secondary" style="max-width: 120px;" :title="p.trek_name">{{ p.trek_name }}</span>
                    <span class="text-secondary tiny-text d-block mt-1" v-if="p.booking_date">
                      <i class="bi bi-clock me-1"></i>{{ formatDateTime(p.booking_date) }}
                    </span>
                  </td>
                  <td class="border-secondary border-opacity-10 text-center">
                    <span class="badge bg-secondary rounded-pill">{{ p.slots }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import { staffService } from '../../services/api';
import { alertService } from '@/services/alert';
import { confirmService } from '@/services/confirm';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'StaffDashboard',
  components: {
    DashboardLayout
  },
  data() {
    return {
      summary: {
        assigned_treks: [],
        today_treks: [],
        participants: []
      },
      loading: true
    };
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-GB', { timeZone: 'Asia/Kolkata' });
      } catch (e) {
        return dateStr;
      }
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
      } catch (e) {
        return dateStr;
      }
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
    async fetchSummary() {
      try {
        const data = await staffService.getDashboardSummary();
        this.summary = data;
      } catch (err) {
        console.error('Failed to load staff summary', err);
      } finally {
        this.loading = false;
      }
    },
    async updateStatus(trekId, newStatus) {
      try {
        await staffService.updateTrekStatus(trekId, newStatus);
        alertService.success('Trek status updated successfully!');
        this.fetchSummary();
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
          this.fetchSummary();
        } catch (err) {
          alertService.error(err.response?.data?.message || 'Failed to close bookings.');
        }
      }
    }
  },
  mounted() {
    this.fetchSummary();
  }
}
</script>

<style scoped>
.stat-icon {
  width: 50px;
  height: 50px;
}
.uppercase-label {
  letter-spacing: 0.8px;
  font-weight: 600;
}
</style>
