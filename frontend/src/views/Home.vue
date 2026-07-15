<template>
  <div class="container py-5">
    <!-- Hero Section -->
    <div class="container py-4 text-center text-lg-start">
      <div class="row align-items-center py-4">
        <div class="col-lg-6">
          <h1 class="display-4 fw-bold mb-3 text-light">
            Manage <span class="text-gradient">trekking trips online.</span>
          </h1>
          <div class="d-flex justify-content-center justify-content-lg-start mb-4">
            <ul class="list-unstyled fs-5 text-secondary text-start mb-0">
              <li class="mb-2"><i class="bi bi-check-circle-fill text-info me-2"></i> Browse available treks</li>
              <li class="mb-2"><i class="bi bi-check-circle-fill text-info me-2"></i> Book treks online</li>
              <li class="mb-2"><i class="bi bi-check-circle-fill text-info me-2"></i> Track booking status easily</li>
            </ul>
          </div>
          <div class="d-flex flex-wrap justify-content-center justify-content-lg-start gap-3">
            <router-link to="/treks" class="btn btn-glow px-4 py-3">Explore Treks</router-link>
            <router-link to="/register" v-if="!isLoggedIn" class="btn btn-outline-secondary border-secondary text-light px-4 py-3">Join as Trekker</router-link>
          </div>
        </div>
        <div class="col-lg-6 mt-5 mt-lg-0 text-center">
          <div class="position-relative d-inline-block">
            <div class="p-4 card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-circle d-inline-flex align-items-center justify-content-center shadow-sm" style="width: 260px; height: 260px;">
              <img src="../assets/images/logo.png" alt="TrekSphere Logo" class="img-fluid" style="max-height: 160px; width: auto;" />
            </div>
            <div class="mt-3">
              <h1 class="display-4 fw-bold mb-3 text-light">Trek<span class="text-gradient">Sphere</span></h1>
              <p>Book your next trekking adventure with TrekSphere</p>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- Quick Stats Section -->
    <h3 class="h4 fw-bold mb-4 mt-5 text-light text-center text-md-start">Statistics</h3>
    <div class="row g-4 mb-5">
      <div class="col-6 col-lg-3">
        <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow-sm rounded p-3 text-center">
          <div class="fs-3 mb-2 text-info"><i class="bi bi-compass"></i></div>
          <h4 class="h2 fw-bold mb-1 text-light">{{ stats.total_treks }}</h4>
          <p class="text-secondary mb-0 small">Total Treks</p>
        </div>
      </div>

      <div class="col-6 col-lg-3">
        <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow-sm rounded p-3 text-center">
          <div class="fs-3 mb-2 text-primary"><i class="bi bi-people"></i></div>
          <h4 class="h2 fw-bold mb-1 text-light">{{ stats.total_trekkers }}</h4>
          <p class="text-secondary mb-0 small">Total Trekkers</p>
        </div>
      </div>
 
      <div class="col-6 col-lg-3">
        <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow-sm rounded p-3 text-center">
          <div class="fs-3 mb-2 text-warning"><i class="bi bi-map"></i></div>
          <h4 class="h2 fw-bold mb-1 text-light">{{ stats.total_staff }}</h4>
          <p class="text-secondary mb-0 small">Trek Leaders</p>
        </div>
      </div>

      <div class="col-6 col-lg-3">
        <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow-sm rounded p-3 text-center">
          <div class="fs-3 mb-2 text-success"><i class="bi bi-calendar-check"></i></div>
          <h4 class="h2 fw-bold mb-1 text-light">{{ stats.total_bookings }}</h4>
          <p class="text-secondary mb-0 small">Bookings Made</p>
        </div>
      </div>
    </div>

    <!-- Featured/Recent Treks Section -->
    <div class="my-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="h4 fw-bold text-light mb-0">Upcoming Indian Treks</h3>
        <router-link to="/treks" class="btn btn-sm btn-outline-secondary text-light">
          View All Treks <i class="bi bi-arrow-right ms-1"></i>
        </router-link>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-info" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="featuredTreks.length === 0" class="text-center py-5 bg-dark bg-opacity-25 border border-secondary border-opacity-10 rounded">
        <p class="text-secondary mb-0">No treks are open for booking right now. Check back soon!</p>
      </div>

      <div v-else class="row g-4">
        <div v-for="trek in featuredTreks" :key="trek.id" class="col-md-6 col-lg-4">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow-sm rounded h-100 d-flex flex-column">
            <div class="card-body d-flex flex-column">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="badge bg-secondary bg-opacity-20 text-light border border-secondary border-opacity-25 py-1 px-2 rounded">{{ trek.difficulty }}</span>
                <span class="text-info small fw-bold">{{ trek.slots_left }} Slots left</span>
              </div>
              <h4 class="card-title h5 fw-bold text-light mb-2">{{ trek.name }}</h4>
              <p class="card-text text-secondary small mb-4 flex-grow-1">
                {{ trek.description || 'Embark on a unique trekking journey exploring pristine nature and scenic views.' }}
              </p>
              
              <div class="mt-auto pt-3 border-top border-secondary border-opacity-10">
                <div class="d-flex justify-content-between align-items-center mb-3 text-secondary small">
                  <span><i class="bi bi-geo-alt text-danger me-1"></i>{{ trek.location }}</span>
                  <span><i class="bi bi-clock text-warning me-1"></i>{{ trek.duration }} Days</span>
                </div>
                <router-link :to="`/treks?id=${trek.id}`" class="btn btn-sm btn-outline-info w-100">View Details</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { publicService, authService } from '../services/api';

export default {
  name: 'Home',
  data() {
    return {
      stats: {
        total_treks: 0,
        total_trekkers: 0,
        total_staff: 0,
        total_bookings: 0
      },
      featuredTreks: [],
      loading: true,
      isLoggedIn: false
    };
  },
  methods: {
    getDifficultyStars(difficulty) {
      const diff = (difficulty || '').toLowerCase();
      if (diff.includes('easy')) return '⭐';
      if (diff.includes('moderate')) return '⭐⭐';
      if (diff.includes('hard') || diff.includes('difficult')) return '⭐⭐⭐';
      return '⭐';
    }
  },
  async mounted() {
    this.isLoggedIn = authService.isAuthenticated();
    
  
    try {
      const statsData = await publicService.getStats();
      this.stats = statsData;
    } catch (err) {
      console.warn('Failed to load live statistics, using defaults.', err);
    }


    try {
      const treksList = await publicService.getTreks();
      this.featuredTreks = treksList.slice(0, 3);
    } catch (err) {
      console.error('Failed to load featured treks.', err);
    } finally {
      this.loading = false;
    }
  }
}
</script>

<style scoped>
.hover-white:hover {
  color: var(--text-main) !important;
}
</style>
