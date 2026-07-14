<template>
  <DashboardLayout role="admin">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-md-6 text-center text-md-start">
        <h1 class="display-6 fw-bold">Welcome, <span class="text-gradient">Admin</span></h1>
        <p class="text-secondary mb-0">System administration control panel</p>
      </div>
      <div class="col-md-6 text-center text-md-end mt-3 mt-md-0">
        <span class="badge bg-secondary bg-opacity-25 text-success border border-success border-opacity-20 py-2 px-3">System Online 🟢</span>
      </div>
    </div>

    <!-- Summary Grid -->
    <h3 class="h4 fw-bold mb-4 text-light">Today's Summary</h3>
    <div class="row g-4 mb-5">
      <!-- Total Treks -->
      <div class="col-6 col-md-3">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-3 h-100">
          <div class="d-flex align-items-center gap-3">
            <div class="fs-2 text-info"><i class="bi bi-compass"></i></div>
            <div>
              <span class="text-secondary small d-block">Total Treks</span>
              <strong class="h3 fw-bold mb-0 text-light">{{ summary.total_treks }}</strong>
            </div>
          </div>
        </div>
      </div>
      <!-- Total Users -->
      <div class="col-6 col-md-3">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-3 h-100">
          <div class="d-flex align-items-center gap-3">
            <div class="fs-2 text-primary"><i class="bi bi-people"></i></div>
            <div>
              <span class="text-secondary small d-block">Trekkers</span>
              <strong class="h3 fw-bold mb-0 text-light">{{ summary.total_users }}</strong>
            </div>
          </div>
        </div>
      </div>
      <!-- Total Bookings -->
      <div class="col-6 col-md-3">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-3 h-100">
          <div class="d-flex align-items-center gap-3">
            <div class="fs-2 text-success"><i class="bi bi-calendar-check"></i></div>
            <div>
              <span class="text-secondary small d-block">Bookings</span>
              <strong class="h3 fw-bold mb-0 text-light">{{ summary.total_bookings }}</strong>
            </div>
          </div>
        </div>
      </div>
      <!-- Total Staff -->
      <div class="col-6 col-md-3">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-3 h-100">
          <div class="d-flex align-items-center gap-3">
            <div class="fs-2 text-warning"><i class="bi bi-map"></i></div>
            <div>
              <span class="text-secondary small d-block">Staff Leaders</span>
              <strong class="h3 fw-bold mb-0 text-light">{{ summary.total_staff }}</strong>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-5">
      <!-- Recent Bookings Table -->
      <div class="col-lg-8">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="h5 fw-bold mb-0 text-light">Recent Bookings</h4>
            <router-link to="/admin/bookings" class="btn btn-outline-info btn-sm rounded-pill px-3">View All</router-link>
          </div>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <div v-else-if="summary.recent_bookings.length === 0" class="text-center py-5">
            <p class="text-secondary mb-0">No booking requests in database.</p>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
              <thead>
                <tr>
                  <th class="text-secondary border-secondary">Trekker</th>
                  <th class="text-secondary border-secondary">Destination</th>
                  <th class="text-secondary border-secondary">Slots</th>
                  <th class="text-secondary border-secondary">Date</th>
                  <th class="text-secondary border-secondary">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="booking in summary.recent_bookings" :key="booking.id">
                  <td class="border-secondary border-opacity-10">
                    <div class="fw-bold text-light">{{ booking.trekker_name }}</div>
                  </td>
                  <td class="border-secondary border-opacity-10 text-light">
                    {{ booking.trek_name }}
                  </td>
                  <td class="border-secondary border-opacity-10 text-secondary">{{ booking.slots_booked }}</td>
                  <td class="small text-secondary border-secondary border-opacity-10">{{ formatDate(booking.booking_date) }}</td>
                  <td class="border-secondary border-opacity-10">
                    <span class="badge" :class="getStatusClass(booking.status)">
                      {{ booking.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="col-lg-4">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100">
          <h4 class="h5 fw-bold mb-4 text-light">Quick Actions</h4>
          <div class="d-flex flex-column gap-3">
            <router-link to="/admin/treks?create=true" class="btn btn-glow text-start py-3 px-4 d-flex justify-content-between align-items-center rounded-3 text-decoration-none">
              <span><i class="bi bi-plus-circle-fill me-2"></i> Create New Trek</span>
              <span><i class="bi bi-arrow-right"></i></span>
            </router-link>
            <router-link to="/admin/staff?create=true" class="btn btn-outline-secondary border-secondary text-light text-start py-3 px-4 d-flex justify-content-between align-items-center rounded-3 text-decoration-none">
              <span><i class="bi bi-person-plus-fill me-2"></i> Register Trek Leader</span>
              <span><i class="bi bi-arrow-right"></i></span>
            </router-link>
            <router-link to="/admin/users" class="btn btn-outline-secondary border-secondary text-light text-start py-3 px-4 d-flex justify-content-between align-items-center rounded-3 text-decoration-none">
              <span><i class="bi bi-people-fill me-2"></i> Manage Trekkers</span>
              <span><i class="bi bi-arrow-right"></i></span>
            </router-link>
            <router-link to="/admin/reports" class="btn btn-outline-secondary border-secondary text-light text-start py-3 px-4 d-flex justify-content-between align-items-center rounded-3 text-decoration-none">
              <span><i class="bi bi-bar-chart-line-fill me-2"></i> View Analytics</span>
              <span><i class="bi bi-arrow-right"></i></span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import { adminService } from '../../services/api';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'AdminDashboard',
  components: {
    DashboardLayout
  },
  data() {
    return {
      summary: {
        total_treks: 0,
        total_users: 0,
        total_bookings: 0,
        total_staff: 0,
        recent_bookings: []
      },
      loading: true
    };
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-GB', { 
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
        case 'Confirmed': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Pending': return 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    }
  },
  async mounted() {
    try {
      const data = await adminService.getDashboardSummary();
      this.summary = data;
    } catch (err) {
      console.error('Failed to load admin summary', err);
    } finally {
      this.loading = false;
    }
  }
}
</script>
