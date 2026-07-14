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
            <small class="text-secondary d-block mt-2">Reservations logged</small>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <h6 class="text-secondary small fw-bold mb-2">Slots Reserved</h6>
            <strong class="display-5 fw-bold text-gradient">{{ stats.metrics.total_slots_booked }}</strong>
            <small class="text-secondary d-block mt-2">Individual trek bookings</small>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <h6 class="text-secondary small fw-bold mb-2">Trekkers (Users)</h6>
            <strong class="display-5 fw-bold text-gradient">{{ stats.metrics.total_users }}</strong>
            <small class="text-secondary d-block mt-2">Registered accounts</small>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <h6 class="text-secondary small fw-bold mb-2">Staff Leaders</h6>
            <strong class="display-5 fw-bold text-gradient">{{ stats.metrics.total_staff }}</strong>
            <small class="text-secondary d-block mt-2">Active guides and guides</small>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <!-- Trek Status Distribution -->
        <div class="col-md-6 col-lg-4">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow h-100">
            <h5 class="fw-bold text-light mb-4"><i class="bi bi-pie-chart-fill text-info me-2"></i>Trek Statuses</h5>
            <div class="position-relative" style="height: 250px;">
              <canvas id="statusChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Difficulty Breakdown -->
        <div class="col-md-6 col-lg-4">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow h-100">
            <h5 class="fw-bold text-light mb-4"><i class="bi bi-graph-up-arrow text-primary me-2"></i>Difficulty Levels</h5>
            <div class="position-relative" style="height: 250px;">
              <canvas id="difficultyChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Popular Treks -->
        <div class="col-md-12 col-lg-4">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow h-100">
            <h5 class="fw-bold text-light mb-4"><i class="bi bi-award-fill text-warning me-2"></i>Popular Treks</h5>
            <div class="position-relative" style="height: 250px;">
              <canvas id="popularChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Booking Trends -->
        <div class="col-12">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow">
            <h5 class="fw-bold text-light mb-4"><i class="bi bi-graph-up text-success me-2"></i>Monthly Booking Trends</h5>
            <div class="position-relative" style="height: 250px;">
              <canvas id="trendsChart"></canvas>
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
import { Chart } from 'chart.js/auto';

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
        booking_trends: [],
        metrics: {
          total_slots_booked: 0,
          total_bookings: 0,
          total_users: 0,
          total_staff: 0
        }
      },
      loading: true,
      chartInstances: []
    };
  },
  methods: {
    async fetchStats() {
      this.loading = true;
      try {
        const data = await adminService.getReportStats();
        this.stats = data;
        this.loading = false;
        this.$nextTick(() => {
          setTimeout(() => {
            this.initCharts();
          }, 150);
        });
      } catch (err) {
        console.error('Failed to load reports stats', err);
        this.loading = false;
      }
    },
    initCharts() {
      this.chartInstances.forEach(c => c.destroy());
      this.chartInstances = [];

      // 1. Trek Status Distribution (Bar Chart)
      const statusData = this.stats.trek_status_distribution || {};
      const statusCtx = document.getElementById('statusChart').getContext('2d');
      const statusChart = new Chart(statusCtx, {
        type: 'bar',
        data: {
          labels: Object.keys(statusData),
          datasets: [{
            label: 'Treks Count',
            data: Object.values(statusData),
            backgroundColor: ['#0dcaf0', '#0a58ca', '#ffc107', '#dc3545', '#198754'],
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#adb5bd' }, grid: { display: false } },
            y: { ticks: { color: '#adb5bd', precision: 0 }, grid: { color: 'rgba(255,255,255,0.05)' } }
          }
        }
      });
      this.chartInstances.push(statusChart);

      // 2. Difficulty Breakdown (Doughnut Chart)
      const diffData = this.stats.difficulty_distribution || {};
      const diffCtx = document.getElementById('difficultyChart').getContext('2d');
      const diffChart = new Chart(diffCtx, {
        type: 'doughnut',
        data: {
          labels: Object.keys(diffData),
          datasets: [{
            data: Object.values(diffData),
            backgroundColor: ['#198754', '#0dcaf0', '#ffc107', '#dc3545'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { color: '#adb5bd' } }
          }
        }
      });
      this.chartInstances.push(diffChart);

      // 3. Popular Treks (Horizontal Bar Chart)
      const topTreks = this.stats.top_treks || [];
      const popCtx = document.getElementById('popularChart').getContext('2d');
      const popChart = new Chart(popCtx, {
        type: 'bar',
        data: {
          labels: topTreks.map(t => t.name),
          datasets: [{
            label: 'Participants',
            data: topTreks.map(t => t.current_participants),
            backgroundColor: 'rgba(255, 193, 7, 0.75)',
            borderColor: '#ffc107',
            borderWidth: 1,
            borderRadius: 4
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#adb5bd' }, grid: { color: 'rgba(255,255,255,0.05)' } },
            y: { ticks: { color: '#adb5bd' }, grid: { display: false } }
          }
        }
      });
      this.chartInstances.push(popChart);

      // 4. Booking Trends (Line Chart)
      const trends = this.stats.booking_trends || [];
      const trendsLabels = trends.length > 0 ? trends.map(t => t.label) : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
      const trendsValues = trends.length > 0 ? trends.map(t => t.count) : [0, 0, 0, 0, 0, 0];

      const trendsCtx = document.getElementById('trendsChart').getContext('2d');
      const trendsChart = new Chart(trendsCtx, {
        type: 'line',
        data: {
          labels: trendsLabels,
          datasets: [{
            label: 'Bookings Count',
            data: trendsValues,
            borderColor: '#198754',
            backgroundColor: 'rgba(25, 135, 84, 0.1)',
            fill: true,
            tension: 0.3,
            borderWidth: 2,
            pointBackgroundColor: '#198754'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#adb5bd' } } },
          scales: {
            x: { ticks: { color: '#adb5bd' }, grid: { color: 'rgba(255,255,255,0.05)' } },
            y: { ticks: { color: '#adb5bd', precision: 0 }, grid: { color: 'rgba(255,255,255,0.05)' } }
          }
        }
      });
      this.chartInstances.push(trendsChart);
    }
  },
  mounted() {
    this.fetchStats();
  },
  beforeUnmount() {
    this.chartInstances.forEach(c => c.destroy());
  }
}
</script>

<style scoped>
/* Chart parent height is managed by standard style parameters */
</style>
