<template>
  <div class="container py-5">
    <!-- Header -->
    <div class="row align-items-center mb-5 text-center text-md-start">
      <div class="col-md-8">
        <h1 class="display-5 fw-bold text-light">TrekSphere <span class="text-gradient">Public Analytics</span></h1>
        <p class="text-secondary mb-0 fs-5">Live statistics, popular destinations, and booking trends on the TrekSphere platform.</p>
      </div>
      <div class="col-md-4 text-md-end mt-3 mt-md-0">
        <router-link to="/register" class="btn btn-glow px-4 py-2">
          <i class="bi bi-person-plus me-1"></i>Join Now & Book
        </router-link>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-info" role="status"></div>
    </div>

    <div v-else>
      <!-- Key Statistics -->
      <div class="row g-4 mb-5">
        <div class="col-6 col-lg-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <div class="fs-3 mb-2 text-info"><i class="bi bi-compass"></i></div>
            <strong class="h2 fw-bold text-gradient d-block">{{ stats.total_treks }}</strong>
            <span class="text-secondary small">Total Treks</span>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <div class="fs-3 mb-2 text-primary"><i class="bi bi-people"></i></div>
            <strong class="h2 fw-bold text-gradient d-block">{{ stats.total_trekkers }}</strong>
            <span class="text-secondary small">Registered Trekkers</span>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <div class="fs-3 mb-2 text-warning"><i class="bi bi-map"></i></div>
            <strong class="h2 fw-bold text-gradient d-block">{{ stats.total_staff }}</strong>
            <span class="text-secondary small">Trek Guides</span>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow text-center">
            <div class="fs-3 mb-2 text-success"><i class="bi bi-calendar-check"></i></div>
            <strong class="h2 fw-bold text-gradient d-block">{{ stats.total_bookings }}</strong>
            <span class="text-secondary small">Bookings Placed</span>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="row g-4">
        <!-- Difficulty Breakdown -->
        <div class="col-md-6 col-lg-4">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow h-100">
            <h5 class="fw-bold text-light mb-4"><i class="bi bi-pie-chart text-info me-2"></i>Trek Difficulty Levels</h5>
            <div class="chart-container position-relative" style="height: 250px;">
              <canvas id="difficultyChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Popular Treks -->
        <div class="col-md-6 col-lg-8">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow h-100">
            <h5 class="fw-bold text-light mb-4"><i class="bi bi-award text-warning me-2"></i>Most Popular Treks (Participants)</h5>
            <div class="chart-container position-relative" style="height: 250px;">
              <canvas id="popularChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Booking Trends -->
        <div class="col-12">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow">
            <h5 class="fw-bold text-light mb-4"><i class="bi bi-graph-up text-success me-2"></i>Monthly Booking Activity</h5>
            <div class="chart-container position-relative" style="height: 300px;">
              <canvas id="trendsChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { publicService } from '../services/api';
import { Chart } from 'chart.js/auto';

export default {
  name: 'PublicDashboard',
  data() {
    return {
      stats: null,
      loading: true,
      chartInstances: []
    };
  },
  methods: {
    async loadStats() {
      this.loading = true;
      try {
        const response = await publicService.getStats();
        this.stats = response;
        this.loading = false;
        this.$nextTick(() => {
          this.initCharts();
        });
      } catch (err) {
        console.error('Failed to load public stats', err);
        this.loading = false;
      }
    },
    initCharts() {
      // 1. Difficulty Doughnut Chart
      const diffData = this.stats.difficulty_distribution || {};
      const diffLabels = Object.keys(diffData);
      const diffValues = Object.values(diffData);

      const diffCtx = document.getElementById('difficultyChart').getContext('2d');
      const diffChart = new Chart(diffCtx, {
        type: 'doughnut',
        data: {
          labels: diffLabels,
          datasets: [{
            data: diffValues,
            backgroundColor: ['#198754', '#0dcaf0', '#ffc107', '#dc3545'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { color: '#adb5bd' }
            }
          }
        }
      });
      this.chartInstances.push(diffChart);

      // 2. Popular Treks Horizontal Bar Chart
      const topTreks = this.stats.top_treks || [];
      const popularLabels = topTreks.map(t => t.name);
      const popularValues = topTreks.map(t => t.current_participants);

      const popCtx = document.getElementById('popularChart').getContext('2d');
      const popChart = new Chart(popCtx, {
        type: 'bar',
        data: {
          labels: popularLabels,
          datasets: [{
            label: 'Slots Booked',
            data: popularValues,
            backgroundColor: 'rgba(13, 202, 240, 0.75)',
            borderColor: '#0dcaf0',
            borderWidth: 1,
            borderRadius: 6
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#adb5bd' }
            },
            y: {
              grid: { display: false },
              ticks: { color: '#adb5bd' }
            }
          }
        }
      });
      this.chartInstances.push(popChart);

      // 3. Line Chart for Booking Trends
      const trends = this.stats.booking_trends || [];
      const trendsLabels = trends.length > 0 ? trends.map(t => t.label) : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
      const trendsValues = trends.length > 0 ? trends.map(t => t.count) : [0, 0, 0, 0, 0, 0];

      const trendsCtx = document.getElementById('trendsChart').getContext('2d');
      const trendsChart = new Chart(trendsCtx, {
        type: 'line',
        data: {
          labels: trendsLabels,
          datasets: [{
            label: 'Monthly Bookings Count',
            data: trendsValues,
            borderColor: '#198754',
            backgroundColor: 'rgba(25, 135, 84, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 2,
            pointBackgroundColor: '#198754'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: '#adb5bd' }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#adb5bd' }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#adb5bd', precision: 0 }
            }
          }
        }
      });
      this.chartInstances.push(trendsChart);
    }
  },
  mounted() {
    this.loadStats();
  },
  beforeUnmount() {
    this.chartInstances.forEach(c => c.destroy());
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
</style>