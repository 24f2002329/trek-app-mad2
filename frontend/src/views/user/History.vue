<template>
  <DashboardLayout role="user">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Trek <span class="text-gradient">History</span></h1>
        <p class="text-secondary mb-0">Review your past journeys, completed adventures, and cancelled registrations.</p>
      </div>
    </div>

    <!-- History Container -->
    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow">
      <h5 class="fw-bold text-light mb-4">Past Trails</h5>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-info" role="status"></div>
      </div>

      <!-- Empty State -->
      <div v-else-if="history.length === 0" class="text-center py-5">
        <span class="display-3 mb-2 d-block text-secondary"><i class="bi bi-clock-history"></i></span>
        <p class="text-secondary">No trek history found.</p>
      </div>

      <!-- History Table -->
      <div v-else class="table-responsive">
        <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
          <thead>
            <tr>
              <th class="text-secondary border-secondary">Trek</th>
              <th class="text-secondary border-secondary">Reserved On</th>
              <th class="text-secondary border-secondary text-center">Slots</th>
              <th class="text-secondary border-secondary">Outcome</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in history" :key="b.booking_id">
              <td class="border-secondary border-opacity-10">
                <div class="fw-bold text-secondary fs-6">{{ b.trek_name }}</div>
                <span class="small text-muted d-block mt-1">
                  📍 {{ b.location }} | ⏳ {{ b.duration }} Days | 📅 Started: {{ formatDate(b.start_date) }}
                </span>
              </td>
              <td class="small text-secondary border-secondary border-opacity-10">
                {{ formatDate(b.booking_date) }}
              </td>
              <td class="border-secondary border-opacity-10 text-center text-secondary">
                {{ b.slots }}
              </td>
              <td class="border-secondary border-opacity-10">
                <span class="badge rounded-pill" :class="getStatusClass(b.status)">{{ getOutcomeLabel(b) }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import { userService } from '../../services/api';
import { alertService } from '@/services/alert';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'UserHistory',
  components: {
    DashboardLayout
  },
  data() {
    return {
      history: [],
      loading: true
    };
  },
  methods: {
    async fetchHistory() {
      this.loading = true;
      try {
        const data = await userService.getDashboardSummary();
        this.history = data.booking_history;
      } catch (err) {
        alertService.error('Failed to load trek history.');
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-GB', { timeZone: 'Asia/Kolkata', day: '2-digit', month: 'short', year: 'numeric' });
      } catch (e) {
        return dateStr;
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 'Confirmed': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Pending': return 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        case 'Completed': return 'bg-info bg-opacity-25 text-info border border-info border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    },
    getOutcomeLabel(b) {
      if (b.status === 'Cancelled') return 'Cancelled';
      if (b.status === 'Confirmed') {
        const today = new Date();
        const start = b.start_date ? new Date(b.start_date) : null;
        if (start && start < today) {
          return 'Completed';
        }
        return 'Confirmed';
      }
      return b.status;
    }
  },
  mounted() {
    this.fetchHistory();
  }
}
</script>
