<template>
  <DashboardLayout role="admin">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">System <span class="text-gradient">Analytics & Reports</span></h1>
        <p class="text-secondary mb-0">Live summaries of platform metrics, trek status distributions, and guides efficiency</p>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-info" role="status"></div>
    </div>

    <div v-else>
      <!-- Key Aggregates -->
      <div class="row g-4 mb-5">
        <div class="col-md-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <h6 class="text-secondary small fw-bold mb-2">Total Bookings</h6>
            <strong class="display-5 fw-bold text-gradient">{{ stats.metrics.total_bookings }}</strong>
            <small class="text-muted d-block mt-2">Reservations logged</small>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <h6 class="text-secondary small fw-bold mb-2">Slots Reserved</h6>
            <strong class="display-5 fw-bold text-gradient">{{ stats.metrics.total_slots_booked }}</strong>
            <small class="text-muted d-block mt-2">Individual trek bookings</small>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <h6 class="text-secondary small fw-bold mb-2">Trekkers (Users)</h6>
            <strong class="display-5 fw-bold text-gradient">{{ stats.metrics.total_users }}</strong>
            <small class="text-muted d-block mt-2">Registered accounts</small>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <h6 class="text-secondary small fw-bold mb-2">Staff Leaders</h6>
            <strong class="display-5 fw-bold text-gradient">{{ stats.metrics.total_staff }}</strong>
            <small class="text-muted d-block mt-2">Active guides and guides</small>
          </div>
        </div>
      </div>

      <div class="row g-5">
        <!-- Trek Status Distribution (Gauges / Visuals) -->
        <div class="col-lg-6">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100">
            <h4 class="h5 fw-bold text-light mb-4"><i class="bi bi-pie-chart-fill text-info me-2"></i>Trek Status Distribution</h4>
            
            <div class="d-flex flex-column gap-3">
              <div v-for="(val, key) in stats.trek_status_distribution" :key="key">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <span class="text-light fw-bold small">{{ key }}</span>
                  <span class="text-secondary small">{{ val }} trek(s)</span>
                </div>
                <div class="progress bg-black bg-opacity-35" style="height: 10px;">
                  <div 
                    class="progress-bar rounded-pill" 
                    :class="getProgressBarClass(key)" 
                    role="progressbar" 
                    :style="{ width: getPercentage(val, totalTreks) + '%' }"
                    :aria-valuenow="val" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
              </div>
              <div v-if="Object.keys(stats.trek_status_distribution).length === 0" class="text-center text-secondary py-4">
                No trek records to analyze.
              </div>
            </div>
          </div>
        </div>

        <!-- Difficulty Distribution -->
        <div class="col-lg-6">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100">
            <h4 class="h5 fw-bold text-light mb-4"><i class="bi bi-graph-up-arrow text-primary me-2"></i>Difficulty Levels Breakdown</h4>
            
            <div class="d-flex align-items-center justify-content-around flex-wrap h-100 py-3">
              <!-- SVG Donut Chart for Difficulty -->
              <div class="donut-chart-container position-relative" style="width: 160px; height: 160px;">
                <svg width="100%" height="100%" viewBox="0 0 42 42" class="donut">
                  <circle class="donut-hole" cx="21" cy="21" r="15.91549430918954" fill="transparent"></circle>
                  <circle class="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#1b2535" stroke-width="3.5"></circle>
                  
                  <!-- Segment 1: Easy -->
                  <circle 
                    class="donut-segment" 
                    cx="21" cy="21" r="15.91549430918954" 
                    fill="transparent" 
                    stroke="#198754" 
                    stroke-width="3.5" 
                    :stroke-dasharray="getDonutSegmentDasharray('Easy')" 
                    stroke-dashoffset="100"
                  ></circle>
                  <!-- Segment 2: Medium -->
                  <circle 
                    class="donut-segment" 
                    cx="21" cy="21" r="15.91549430918954" 
                    fill="transparent" 
                    stroke="#00f2fe" 
                    stroke-width="3.5" 
                    :stroke-dasharray="getDonutSegmentDasharray('Medium')" 
                    :stroke-dashoffset="getDonutSegmentDashoffset('Medium')"
                  ></circle>
                  <!-- Segment 3: Hard -->
                  <circle 
                    class="donut-segment" 
                    cx="21" cy="21" r="15.91549430918954" 
                    fill="transparent" 
                    stroke="#ffc107" 
                    stroke-width="3.5" 
                    :stroke-dasharray="getDonutSegmentDasharray('Hard')" 
                    :stroke-dashoffset="getDonutSegmentDashoffset('Hard')"
                  ></circle>
                  <!-- Segment 4: Expert -->
                  <circle 
                    class="donut-segment" 
                    cx="21" cy="21" r="15.91549430918954" 
                    fill="transparent" 
                    stroke="#dc3545" 
                    stroke-width="3.5" 
                    :stroke-dasharray="getDonutSegmentDasharray('Expert')" 
                    :stroke-dashoffset="getDonutSegmentDashoffset('Expert')"
                  ></circle>
                </svg>
                <div class="donut-center text-center">
                  <div class="h5 mb-0 fw-bold text-light">{{ totalTreks }}</div>
                  <div class="tiny-text text-secondary">Treks</div>
                </div>
              </div>

              <!-- Legends -->
              <div class="d-flex flex-column gap-2">
                <div class="d-flex align-items-center gap-2 small">
                  <span class="legend-color rounded-circle" style="background-color: #198754; width: 12px; height: 12px; display: inline-block;"></span>
                  <span class="text-secondary">Easy: <strong class="text-light">{{ getDifficultyCount('Easy') }}</strong></span>
                </div>
                <div class="d-flex align-items-center gap-2 small">
                  <span class="legend-color rounded-circle" style="background-color: #00f2fe; width: 12px; height: 12px; display: inline-block;"></span>
                  <span class="text-secondary">Medium: <strong class="text-light">{{ getDifficultyCount('Medium') }}</strong></span>
                </div>
                <div class="d-flex align-items-center gap-2 small">
                  <span class="legend-color rounded-circle" style="background-color: #ffc107; width: 12px; height: 12px; display: inline-block;"></span>
                  <span class="text-secondary">Hard: <strong class="text-light">{{ getDifficultyCount('Hard') }}</strong></span>
                </div>
                <div class="d-flex align-items-center gap-2 small">
                  <span class="legend-color rounded-circle" style="background-color: #dc3545; width: 12px; height: 12px; display: inline-block;"></span>
                  <span class="text-secondary">Expert: <strong class="text-light">{{ getDifficultyCount('Expert') }}</strong></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Treks by reservations -->
        <div class="col-lg-12">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4">
            <h4 class="h5 fw-bold text-light mb-4"><i class="bi bi-award-fill text-warning me-2"></i>Most Popular Treks (Participation Rates)</h4>
            
            <div v-if="stats.top_treks.length === 0" class="text-center text-secondary py-4">
              No reservation logs available to analyze popularity rankings.
            </div>

            <div v-else class="row g-4">
              <div class="col-md-6" v-for="trek in stats.top_treks" :key="trek.id">
                <div class="p-3 bg-black bg-opacity-25 rounded-3 border border-secondary border-opacity-10 h-100">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                      <h6 class="fw-bold text-light mb-0">{{ trek.name }}</h6>
                      <small class="text-secondary"><i class="bi bi-geo-alt me-1 text-danger"></i>{{ trek.location }}</small>
                    </div>
                    <span class="badge bg-secondary bg-opacity-20 text-info border border-info border-opacity-25">
                      {{ getPercentage(trek.current_participants, trek.max_slots) }}% Filled
                    </span>
                  </div>
                  <div class="progress bg-black bg-opacity-35 mb-2" style="height: 8px;">
                    <div 
                      class="progress-bar bg-gradient rounded-pill" 
                      role="progressbar" 
                      :style="{ width: getPercentage(trek.current_participants, trek.max_slots) + '%' }"
                    ></div>
                  </div>
                  <div class="d-flex justify-content-between text-secondary small">
                    <span>Reserved: <strong>{{ trek.current_participants }} Slots</strong></span>
                    <span>Max Limit: {{ trek.max_slots }}</span>
                  </div>
                </div>
              </div>
            </div>
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
  name: 'AdminReports',
  components: {
    DashboardLayout
  },
  data() {
    return {
      stats: {
        difficulty_distribution: {},
        trek_status_distribution: {},
        booking_status_distribution: {},
        top_treks: [],
        metrics: {
          total_slots_booked: 0,
          total_bookings: 0,
          total_users: 0,
          total_staff: 0
        }
      },
      loading: true
    };
  },
  computed: {
    totalTreks() {
      return Object.values(this.stats.trek_status_distribution).reduce((a, b) => a + b, 0) || 0;
    }
  },
  methods: {
    async fetchStats() {
      this.loading = true;
      try {
        const data = await adminService.getReportStats();
        this.stats = data;
      } catch (err) {
        console.error('Failed to load reports stats', err);
      } finally {
        this.loading = false;
      }
    },
    getPercentage(val, total) {
      if (!total) return 0;
      return Math.round((val / total) * 100);
    },
    getProgressBarClass(status) {
      switch (status) {
        case 'Open': return 'bg-success';
        case 'Approved': return 'bg-info';
        case 'Pending': return 'bg-warning';
        case 'Closed': return 'bg-danger';
        case 'Completed': return 'bg-primary';
        default: return 'bg-secondary';
      }
    },
    getDifficultyCount(diff) {
      return this.stats.difficulty_distribution[diff] || 0;
    },
    // Donut segment math helper
    getDonutSegmentDasharray(diff) {
      const count = this.getDifficultyCount(diff);
      const percentage = this.getPercentage(count, this.totalTreks);
      return `${percentage} ${100 - percentage}`;
    },
    getDonutSegmentDashoffset(diff) {
      // Find order to stack segments: Easy -> Medium -> Hard -> Expert
      const order = ['Easy', 'Medium', 'Hard', 'Expert'];
      let cumulativeOffset = 100; // Start offset
      
      const targetIndex = order.indexOf(diff);
      for (let i = 0; i < targetIndex; i++) {
        const prevDiff = order[i];
        const prevCount = this.getDifficultyCount(prevDiff);
        const prevPercentage = this.getPercentage(prevCount, this.totalTreks);
        cumulativeOffset -= prevPercentage;
      }
      return cumulativeOffset;
    }
  },
  mounted() {
    this.fetchStats();
  }
}
</script>

<style scoped>
.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.donut {
  transform: rotate(-90deg);
}

.bg-gradient {
  background: linear-gradient(135deg, #00f2fe, #4facfe) !important;
}
</style>
