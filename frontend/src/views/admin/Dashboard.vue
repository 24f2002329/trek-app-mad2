<template>
  <DashboardLayout role="admin">

    <div class="row align-items-center mb-5">
      <div class="col-md-6 text-center text-md-start">
        <h1 class="display-6 fw-bold">Welcome, <span class="text-gradient">Admin</span></h1>
        <p class="text-secondary mb-0">System administration control panel</p>
      </div>
      <div class="col-md-6 text-center text-md-end mt-3 mt-md-0">
        <div class="d-inline-block position-relative" ref="statusDropdown">
          <button 
            class="badge-btn d-inline-flex align-items-center gap-2 py-2 px-3 rounded-pill border bg-secondary bg-opacity-25"
            :class="systemStatusClass"
            @click="toggleDropdown"
            style="font-family: inherit; font-size: 0.85rem; transition: all 0.3s ease;"
          >
            <i class="bi bi-circle-fill" :class="[systemStatusDotClass, { 'pulse-animation': overallStatus === 'online' }]" style="font-size: 0.55rem;"></i>
            <span>System: <strong class="text-capitalize">{{ overallStatus }}</strong></span>
            <i class="bi bi-chevron-down small transition-transform" :class="{'rotate-180': showDropdown}"></i>
          </button>
          
          <div 
            v-if="showDropdown" 
            class="position-absolute end-0 mt-2 p-3 bg-dark border border-secondary border-opacity-25 rounded-4 shadow-lg text-start dropdown-card"
            style="z-index: 1050; min-width: 260px; backdrop-filter: blur(10px);"
          >
            <div class="d-flex justify-content-between align-items-center mb-3">
              <span class="fw-bold text-light small">System Status</span>
              <button 
                class="btn btn-sm btn-icon text-secondary hover-info p-0" 
                @click="refreshStatus"
                :disabled="checkingStatus"
                title="Refresh Status"
              >
                <i class="bi bi-arrow-clockwise d-inline-block" :class="{'spin-animation': checkingStatus}"></i>
              </button>
            </div>
            
            <div class="d-flex flex-column gap-2">
              <div class="d-flex justify-content-between align-items-center py-1 border-bottom border-secondary border-opacity-10">
                <span class="text-secondary small"><i class="bi bi-server me-1"></i> API Service</span>
                <span class="badge rounded-pill small py-1 px-2 border" :class="getStatusBadgeClass(statusDetails.api)">{{ statusDetails.api }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center py-1 border-bottom border-secondary border-opacity-10">
                <span class="text-secondary small"><i class="bi bi-database me-1"></i> Database</span>
                <span class="badge rounded-pill small py-1 px-2 border" :class="getStatusBadgeClass(statusDetails.database)">{{ statusDetails.database }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center py-1 border-bottom border-secondary border-opacity-10">
                <span class="text-secondary small"><i class="bi bi-lightning-fill me-1"></i> Redis Cache</span>
                <span class="badge rounded-pill small py-1 px-2 border" :class="getStatusBadgeClass(statusDetails.redis)">{{ statusDetails.redis }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center py-1">
                <span class="text-secondary small"><i class="bi bi-cpu me-1"></i> Celery Worker</span>
                <span class="badge rounded-pill small py-1 px-2 border" :class="getStatusBadgeClass(statusDetails.celery)">{{ statusDetails.celery }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Grid -->
    <h3 class="h4 fw-bold mb-4 text-light">Summary</h3>
    <div class="row g-4 mb-5">

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
    
    <div class="row g-4 mb-5">
      <div class="col-6 col-md-3">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-3 h-100">
          <div class="d-flex align-items-center gap-3">
            <div class="fs-2 text-warning"><i class="bi bi-hourglass-split"></i></div>
            <div>
              <span class="text-secondary small d-block">Pending Approvals</span>
              <strong class="h3 fw-bold mb-0 text-warning">{{ summary.pending_approvals }}</strong>
            </div>
          </div>
        </div>
      </div>

      <div class="col-6 col-md-3">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-3 h-100">
          <div class="d-flex align-items-center gap-3">
            <div class="fs-2 text-info"><i class="bi bi-calendar-event"></i></div>
            <div>
              <span class="text-secondary small d-block">Upcoming Treks</span>
              <strong class="h3 fw-bold mb-0 text-light">{{ summary.upcoming_treks }}</strong>
            </div>
          </div>
        </div>
      </div>

      <div class="col-6 col-md-3">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-3 h-100">
          <div class="d-flex align-items-center gap-3">
            <div class="fs-2 text-danger"><i class="bi bi-play-circle-fill"></i></div>
            <div>
              <span class="text-secondary small d-block">Starting Today</span>
              <strong class="h3 fw-bold mb-0 text-danger">{{ summary.treks_starting_today }}</strong>
            </div>
          </div>
        </div>
      </div>

      <div class="col-6 col-md-3">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-3 h-100">
          <div class="d-flex align-items-center gap-3">
            <div class="fs-2 text-warning"><i class="bi bi-x-circle-fill"></i></div>
            <div>
              <span class="text-secondary small d-block">Cancelled Bookings</span>
              <strong class="h3 fw-bold mb-0 text-warning">{{ summary.cancelled_bookings }}</strong>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-5">

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

          <!-- Desktop -->
          <div class="d-none d-md-block table-responsive">
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
          <!-- Mobile -->
          <div class="d-md-none table-responsive">
            <table class="table table-dark table-sm border-secondary border-opacity-10 align-middle">
              <thead>
                <tr>
                  <th class="text-secondary border-secondary">Trekker / Trek</th>
                  <th class="text-secondary border-secondary text-end">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="booking in summary.recent_bookings" :key="booking.id">
                  <td class="border-secondary border-opacity-10">
                    <div class="text-light small fw-bold text-truncate" style="max-width: 140px;">{{ booking.trekker_name }}</div>
                    <span class="text-secondary d-block text-truncate" style="font-size:.7rem; max-width: 140px;">{{ booking.trek_name }}</span>
                  </td>
                  <td class="border-secondary border-opacity-10 text-end">
                    <span class="badge rounded-pill" :class="getStatusClass(booking.status)" style="font-size:.65rem;">{{ booking.status }}</span>
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
        pending_approvals: 0,
        upcoming_treks: 0,
        treks_starting_today: 0,
        cancelled_bookings: 0,
        recent_bookings: []
      },
      loading: true,
      showDropdown: false,
      checkingStatus: false,
      overallStatus: 'checking',
      statusDetails: {
        api: 'checking',
        database: 'checking',
        redis: 'checking',
        celery: 'checking'
      }
    };
  },
  computed: {
    systemStatusClass() {
      return {
        'status-online': this.overallStatus === 'online',
        'status-degraded': this.overallStatus === 'degraded',
        'status-offline': this.overallStatus === 'offline',
        'status-checking': this.overallStatus === 'checking'
      };
    },
    systemStatusDotClass() {
      return {
        'text-success': this.overallStatus === 'online',
        'text-warning': this.overallStatus === 'degraded',
        'text-danger': this.overallStatus === 'offline',
        'text-secondary': this.overallStatus === 'checking'
      };
    }
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
        case 'Booked': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Pending': return 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    },
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
      if (this.showDropdown) {
        this.fetchStatus();
      }
    },
    refreshStatus() {
      this.fetchStatus(true);
    },
    async fetchStatus(forceRefresh = false) {
      if (this.checkingStatus) return;
      this.checkingStatus = true;
      try {
        const response = await adminService.getSystemStatus();
        this.overallStatus = response.overall;
        this.statusDetails = response.details;
      } catch (err) {
        console.error('Failed to fetch system status', err);
        this.overallStatus = 'offline';
        this.statusDetails = {
          api: 'offline',
          database: 'offline',
          redis: 'offline',
          celery: 'offline'
        };
      } finally {
        this.checkingStatus = false;
      }
    },
    handleOutsideClick(e) {
      const el = this.$refs.statusDropdown;
      if (el && !el.contains(e.target)) {
        this.showDropdown = false;
      }
    },
    getStatusBadgeClass(status) {
      if (status === 'online') {
        return 'bg-success bg-opacity-25 text-success border-success border-opacity-20';
      } else if (status === 'offline') {
        return 'bg-danger bg-opacity-25 text-danger border-danger border-opacity-20';
      } else if (status === 'checking') {
        return 'bg-secondary bg-opacity-25 text-secondary border-secondary border-opacity-20';
      } else {
        return 'bg-warning bg-opacity-25 text-warning border-warning border-opacity-20';
      }
    }
  },
  async mounted() {
    this.fetchStatus();
    document.addEventListener('click', this.handleOutsideClick);
    
    try {
      const data = await adminService.getDashboardSummary();
      this.summary = data;
    } catch (err) {
      console.error('Failed to load admin summary', err);
    } finally {
      this.loading = false;
    }
  },
  unmounted() {
    document.removeEventListener('click', this.handleOutsideClick);
  }
}
</script>

<style scoped>
.badge-btn {
  background: rgba(33, 37, 41, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.85);
  cursor: pointer;
  outline: none;
  font-weight: 500;
}

.badge-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.badge-btn.status-online {
  color: #198754;
  border-color: rgba(25, 135, 84, 0.3) !important;
}

.badge-btn.status-degraded {
  color: #ffc107;
  border-color: rgba(255, 193, 7, 0.3) !important;
}

.badge-btn.status-offline {
  color: #dc3545;
  border-color: rgba(220, 53, 69, 0.3) !important;
}

.badge-btn.status-checking {
  color: #6c757d;
  border-color: rgba(108, 117, 125, 0.3) !important;
}

.pulse-animation {
  animation: pulse 2.5s infinite ease-in-out;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.65; }
  50% { transform: scale(1.15); opacity: 1; }
  100% { transform: scale(1); opacity: 0.65; }
}

.spin-animation {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.rotate-180 {
  transform: rotate(180deg);
}

.transition-transform {
  transition: transform 0.25s ease;
}

.hover-info {
  transition: color 0.2s ease;
}

.hover-info:hover {
  color: #0dcaf0 !important;
}

.btn-icon {
  background: none;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.btn-icon:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.05);
}

.dropdown-card {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
}
</style>
