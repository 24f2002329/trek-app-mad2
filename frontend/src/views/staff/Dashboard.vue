<template>
  <div class="container py-5">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-md-8 text-center text-md-start">
        <h1 class="display-6 fw-bold">Welcome, <span class="text-gradient">Trek Leader</span></h1>
        <p class="text-secondary mb-0">Assigned expeditions & participant logs</p>
      </div>
      <div class="col-md-4 text-center text-md-end mt-3 mt-md-0">
        <span class="badge bg-info bg-opacity-10 text-info border border-info border-opacity-25 py-2 px-3">Role: Staff Guide <i class="bi bi-compass-fill ms-1"></i></span>
      </div>
    </div>

    <!-- Alert for Today's Treks -->
    <div class="mb-5" v-if="summary.today_treks.length > 0">
      <h4 class="h5 fw-bold text-gradient mb-3"><i class="bi bi-lightning-charge-fill text-warning me-1"></i> Active Today</h4>
      <div class="row g-3">
        <div class="col-md-6" v-for="t in summary.today_treks" :key="t.id">
          <div class="card bg-info bg-opacity-10 border-info border-opacity-25 rounded-3 p-3 d-flex flex-row justify-content-between align-items-center">
            <div>
              <strong class="text-light">{{ t.name }}</strong>
              <div class="small text-secondary">📍 {{ t.location }}</div>
            </div>
            <span class="badge bg-info bg-opacity-20 text-info">{{ t.status }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <!-- Left Column: Assigned Treks -->
      <div class="col-lg-7">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100">
          <h4 class="h5 fw-bold mb-4 text-light">Assigned Expeditions</h4>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <div v-else-if="summary.assigned_treks.length === 0" class="text-center py-5">
            <span class="display-4 d-block mb-3 text-secondary"><i class="bi bi-journal-x"></i></span>
            <p class="text-secondary mb-0">No treks assigned to you yet.</p>
          </div>

          <div v-else class="d-flex flex-column gap-3">
            <div v-for="trek in summary.assigned_treks" :key="trek.id" class="p-3 rounded-3 bg-black bg-opacity-25 border border-secondary border-opacity-10">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                  <h5 class="fw-bold text-light mb-1">{{ trek.name }}</h5>
                  <span class="small text-secondary">📍 {{ trek.location }} | 📅 {{ formatDate(trek.start_date) }}</span>
                </div>
                <span class="badge" :class="getStatusClass(trek.status)">{{ trek.status }}</span>
              </div>
              
              <div class="d-flex justify-content-between align-items-center mt-3 pt-3 border-top border-secondary border-opacity-10">
                <div class="small text-secondary">
                  Slots Booked: <strong class="text-light">{{ trek.current_participants }} / {{ trek.max_slots }}</strong>
                </div>
                
                <!-- Status Update Action -->
                <div class="d-flex align-items-center gap-2">
                  <span class="small text-secondary">Update Status:</span>
                  <select :value="trek.status" @change="updateStatus(trek.id, $event.target.value)" class="form-select form-select-sm bg-dark text-light border-secondary py-1 px-2" style="width: auto;">
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

      <!-- Right Column: Participant Logs -->
      <div class="col-lg-5">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100">
          <h4 class="h5 fw-bold mb-4 text-light">Trekkers Roster</h4>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <div v-else-if="summary.participants.length === 0" class="text-center py-5">
            <span class="display-4 d-block mb-3 text-secondary"><i class="bi bi-people"></i></span>
            <p class="text-secondary mb-0">No participants registered for your treks yet.</p>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
              <thead>
                <tr>
                  <th class="text-secondary border-secondary">Name</th>
                  <th class="text-secondary border-secondary">Trek</th>
                  <th class="text-secondary border-secondary">Slots</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(p, idx) in summary.participants" :key="idx">
                  <td class="border-secondary border-opacity-10">
                    <div class="fw-bold text-light">{{ p.trekker_name }}</div>
                    <span class="small text-secondary">{{ p.email }}</span>
                  </td>
                  <td class="border-secondary border-opacity-10 text-light">
                    <span class="small">{{ p.trek_name }}</span>
                  </td>
                  <td class="border-secondary border-opacity-10">
                    <span class="badge bg-secondary">{{ p.slots }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { staffService } from '../../services/api';

export default {
  name: 'StaffDashboard',
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
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
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
        alert('Trek status updated successfully!');
        this.fetchSummary();
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to update status.');
      }
    }
  },
  mounted() {
    this.fetchSummary();
  }
}
</script>
