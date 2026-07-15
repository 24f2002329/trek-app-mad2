<template>
  <DashboardLayout role="user">
    <div class="row align-items-center mb-5">
      <div class="col-md-6 text-center text-md-start">
        <h1 class="display-6 fw-bold">Hello, <span class="text-gradient">{{ userName }}</span></h1>
        <p class="text-secondary mb-0">Ready for your next adventure?</p>
      </div>
      <div class="col-md-6 text-center text-md-end mt-3 mt-md-0 d-flex justify-content-center justify-content-md-end align-items-center gap-3">
        <span 
          class="badge bg-secondary bg-opacity-25 border py-2 px-3 rounded-pill d-inline-flex align-items-center gap-2"
          :class="isOffline ? 'border-danger border-opacity-30 text-danger' : 'border-success border-opacity-30 text-success'"
        >
          <span 
            class="d-inline-block rounded-circle status-dot" 
            :class="isOffline ? 'bg-danger text-danger' : 'bg-success text-success'" 
            style="width: 7px; height: 7px;"
          ></span>
          System {{ isOffline ? 'Offline' : 'Online' }}
        </span>
        <router-link to="/browse-treks" class="btn btn-glow px-4 py-2">Explore More Treks</router-link>
      </div>
    </div>

    <div class="row g-4">
      <!-- Active Bookings & Upcoming depatures -->
      <div class="col-lg-8">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 mb-4" v-if="summary.upcoming_treks.length > 0">
          <h4 class="h5 fw-bold mb-3 text-info"><i class="bi bi-compass-fill text-info me-1"></i> Next Departure</h4>
          <div class="p-3 rounded-3 bg-black bg-opacity-20 border border-info border-opacity-25 d-flex flex-wrap justify-content-between align-items-center gap-3">
            <div>
              <h5 class="fw-bold text-light mb-1">{{ summary.upcoming_treks[0].trek_name }}</h5>
              <div class="small text-secondary"><i class="bi bi-geo-alt me-1 text-danger"></i>{{ summary.upcoming_treks[0].location }} | <i class="bi bi-calendar-event me-1 text-warning"></i>Starts: {{ formatDate(summary.upcoming_treks[0].start_date) }}</div>
            </div>
            <div class="text-end">
              <span class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-25 mb-1 d-block">{{ summary.upcoming_treks[0].status }}</span>
              <small class="text-secondary">{{ summary.upcoming_treks[0].slots }} slot(s) reserved</small>
            </div>
          </div>
        </div>


        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4">
          <h4 class="h5 fw-bold mb-4 text-light">My Current Bookings</h4>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <div v-else-if="summary.my_bookings.length === 0" class="text-center py-5">
            <span class="display-3 mb-2 d-block text-secondary"><i class="bi bi-calendar-x"></i></span>
            <p class="text-secondary">You haven't booked any treks yet.</p>
            <router-link to="/browse-treks" class="btn btn-outline-secondary border-secondary text-light btn-sm px-3 rounded-3">Find a Trek</router-link>
          </div>

          <template v-else>
            <!-- Desktop -->
            <div class="d-none d-md-block table-responsive">
              <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
                <thead>
                  <tr>
                    <th class="text-secondary border-secondary">Destination</th>
                    <th class="text-secondary border-secondary">Booked On</th>
                    <th class="text-secondary border-secondary">Slots</th>
                    <th class="text-secondary border-secondary">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="b in summary.my_bookings" :key="b.booking_id">
                    <td class="border-secondary border-opacity-10">
                      <div class="fw-bold text-light">{{ b.trek_name }}</div>
                      <span class="small text-secondary"><i class="bi bi-geo-alt me-1 text-danger"></i>{{ b.location }} | <i class="bi bi-clock me-1 text-info"></i>{{ b.duration }} Days</span>
                    </td>
                    <td class="small text-secondary border-secondary border-opacity-10">{{ formatDate(b.booking_date) }}</td>
                    <td class="border-secondary border-opacity-10 text-secondary">{{ b.slots }}</td>
                    <td class="border-secondary border-opacity-10">
                      <span class="badge" :class="getStatusClass(b.status)">{{ b.status }}</span>
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
                    <th class="text-secondary border-secondary">Destination</th>
                    <th class="text-secondary border-secondary text-end">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="b in summary.my_bookings" :key="b.booking_id">
                    <td class="border-secondary border-opacity-10">
                      <div class="text-light small fw-bold text-truncate" style="max-width: 150px;">{{ b.trek_name }}</div>
                      <span class="text-secondary d-block" style="font-size:.7rem;"><i class="bi bi-geo-alt me-1 text-danger"></i>{{ b.location }}</span>
                    </td>
                    <td class="border-secondary border-opacity-10 text-end">
                      <span class="badge rounded-pill" :class="getStatusClass(b.status)" style="font-size:.65rem;">{{ b.status }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
        </div>

        <!-- Booking History Card -->
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 mt-4">
          <h4 class="h5 fw-bold mb-4 text-light">Trek History</h4>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <div v-else-if="summary.booking_history.length === 0" class="text-center py-4">
            <p class="text-secondary small mb-0">No past or cancelled bookings.</p>
          </div>

          <template v-else>
            <!-- Desktop -->
            <div class="d-none d-md-block table-responsive">
              <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
                <thead>
                  <tr>
                    <th class="text-secondary border-secondary">Destination</th>
                    <th class="text-secondary border-secondary">Slots</th>
                    <th class="text-secondary border-secondary">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="b in summary.booking_history" :key="b.booking_id">
                    <td class="border-secondary border-opacity-10">
                      <div class="fw-bold text-secondary">{{ b.trek_name }}</div>
                      <span class="small text-secondary"><i class="bi bi-geo-alt me-1 text-danger "></i>{{ b.location }}</span>
                    </td>
                    <td class="border-secondary border-opacity-10 text-secondary">{{ b.slots }}</td>
                    <td class="border-secondary border-opacity-10">
                      <span class="badge" :class="getStatusClass(b.status)">{{ b.status }}</span>
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
                    <th class="text-secondary border-secondary">Trek</th>
                    <th class="text-secondary border-secondary text-end">Outcome</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="b in summary.booking_history" :key="b.booking_id">
                    <td class="border-secondary border-opacity-10">
                      <div class="text-secondary small fw-bold text-truncate" style="max-width: 150px;">{{ b.trek_name }}</div>
                      <span class="text-secondary d-block" style="font-size:.7rem;"><i class="bi bi-geo-alt me-1 text-danger"></i>{{ b.location }}</span>
                    </td>
                    <td class="border-secondary border-opacity-10 text-end">
                      <span class="badge rounded-pill" :class="getStatusClass(b.status)" style="font-size:.65rem;">{{ b.status }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
        </div>
      </div>

      <!-- Recommended Treks -->
      <div class="col-lg-4">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100">
          <h4 class="h5 fw-bold mb-4 text-light">Recommended for You</h4>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-info" role="status"></div>
          </div>

          <div v-else-if="summary.recommended_treks.length === 0" class="text-center py-5">
            <p class="text-secondary mb-0">No new recommendations right now.</p>
          </div>

          <div v-else class="d-flex flex-column gap-3">
            <div v-for="trek in summary.recommended_treks" :key="trek.id" class="p-3 rounded-3 bg-black bg-opacity-25 border border-secondary border-opacity-10">
              <span class="badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-50 px-2 py-1 mb-2 rounded-pill">{{ trek.difficulty }}</span>
              <h5 class="fw-bold text-light mb-1">{{ trek.name }}</h5>
              <div class="small text-secondary mb-3"><i class="bi bi-geo-alt me-1 text-danger"></i>{{ trek.location }} | <i class="bi bi-clock me-1 text-info"></i>{{ trek.duration }} Days</div>
              
              <div class="d-flex justify-content-between align-items-center">
                <span class="small text-info">{{ trek.slots_left }} spots left</span>
                <router-link :to="`/browse-treks?id=${trek.id}`" class="btn btn-glow btn-sm py-1 px-3">Book Now</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import { userService, authService, publicService } from '../../services/api';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'UserDashboard',
  components: {
    DashboardLayout
  },
  data() {
    return {
      userName: '',
      summary: {
        upcoming_treks: [],
        my_bookings: [],
        booking_history: [],
        recommended_treks: []
      },
      loading: true,
      isOffline: false
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
    getStatusClass(status) {
      switch (status) {
        case 'Booked': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Pending': return 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        case 'Completed': return 'bg-secondary bg-opacity-25 text-secondary border border-secondary border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    },
    async checkSystemStatus() {
      try {
        const data = await publicService.getSystemStatus();
        this.isOffline = data.status !== 'online';
      } catch (err) {
        this.isOffline = true;
      }
    }
  },
  async mounted() {
    const user = authService.getCurrentUser();
    this.userName = user ? user.name : 'Trekker';
    this.checkSystemStatus();

    try {
      const data = await userService.getDashboardSummary();
      this.summary = data;
    } catch (err) {
      console.error('Failed to load user summary', err);
    } finally {
      this.loading = false;
    }
  }
}
</script>

<style scoped>
.status-dot {
  box-shadow: 0 0 6px currentColor;
  animation: blink 2.5s infinite ease-in-out;
}
@keyframes blink {
  0% { opacity: 0.45; }
  50% { opacity: 1; }
  100% { opacity: 0.45; }
}
</style>
