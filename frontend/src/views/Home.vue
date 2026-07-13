<template>
  <div class="pb-5">
    <!-- Hero Section -->
    <div class="container py-5 text-center text-lg-start">
      <div class="row align-items-center py-5">
        <div class="col-lg-6">
          <h1 class="display-3 fw-bold mb-3">
            Discover <span class="text-gradient">Amazing Treks</span>
          </h1>
          <p class="lead text-secondary mb-4 fs-4">
            Book your next adventure today. Explore breathtaking landscapes, push your limits, and create unforgettable memories with certified guides.
          </p>
          <div class="d-flex flex-wrap justify-content-center justify-content-lg-start gap-3">
            <router-link to="/treks" class="btn btn-glow px-4 py-3">Explore Treks</router-link>
            <router-link to="/register" v-if="!isLoggedIn" class="btn btn-outline-secondary border-secondary text-light px-4 py-3">Join as Trekker</router-link>
          </div>
        </div>
        <div class="col-lg-6 mt-5 mt-lg-0 text-center">
          <div class="position-relative d-inline-block">
            <div class="position-absolute top-50 start-50 translate-middle rounded-circle" style="width: 300px; height: 300px; background: rgba(0, 242, 254, 0.08); filter: blur(50px);"></div>
            <div class="p-4 card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-circle d-inline-flex align-items-center justify-content-center shadow-lg" style="width: 280px; height: 280px;">
              <img src="../assets/images/logo.png" alt="TrekSphere Logo" class="img-fluid" style="max-height: 180px; width: auto;" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Statistics Section -->
    <div class="container my-5">
      <div class="row g-4">
        <!-- Stat 1 -->
        <div class="col-6 col-lg-3">
          <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow rounded-4 p-4 text-center">
            <div class="fs-2 mb-3 text-info"><i class="bi bi-compass"></i></div>
            <h3 class="h1 fw-bold mb-1 text-gradient">{{ stats.total_treks }}</h3>
            <p class="text-secondary mb-0 fw-medium">Treks</p>
          </div>
        </div>
        <!-- Stat 2 -->
        <div class="col-6 col-lg-3">
          <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow rounded-4 p-4 text-center">
            <div class="fs-2 mb-3 text-primary"><i class="bi bi-people"></i></div>
            <h3 class="h1 fw-bold mb-1 text-gradient">{{ stats.total_trekkers }}</h3>
            <p class="text-secondary mb-0 fw-medium">Trekkers</p>
          </div>
        </div>
        <!-- Stat 3 -->
        <div class="col-6 col-lg-3">
          <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow rounded-4 p-4 text-center">
            <div class="fs-2 mb-3 text-warning"><i class="bi bi-map"></i></div>
            <h3 class="h1 fw-bold mb-1 text-gradient">{{ stats.total_staff }}</h3>
            <p class="text-secondary mb-0 fw-medium">Trek Leaders</p>
          </div>
        </div>
        <!-- Stat 4 -->
        <div class="col-6 col-lg-3">
          <div class="card bg-dark bg-opacity-75 border-secondary border-opacity-25 shadow rounded-4 p-4 text-center">
            <div class="fs-2 mb-3 text-success"><i class="bi bi-calendar-check"></i></div>
            <h3 class="h1 fw-bold mb-1 text-gradient">{{ stats.total_bookings }}</h3>
            <p class="text-secondary mb-0 fw-medium">Bookings</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Featured Treks Section -->
    <div class="container my-5 py-4">
      <div class="d-flex flex-wrap justify-content-between align-items-end mb-5">
        <div>
          <h2 class="display-5 fw-bold mb-1">Featured <span class="text-gradient">Treks</span></h2>
          <p class="text-secondary mb-0">Get ready for upcoming open group expeditions</p>
        </div>
        <div class="mt-3 mt-md-0">
          <router-link to="/treks" class="btn btn-outline-secondary border-secondary text-light px-4 py-2 rounded-pill">
            View All Treks <i class="bi bi-arrow-right ms-1"></i>
          </router-link>
        </div>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-info" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="featuredTreks.length === 0" class="text-center py-5">
        <p class="text-secondary">No featured treks available at the moment. Check back soon!</p>
      </div>

      <div v-else class="row g-4 justify-content-center">
        <div v-for="trek in featuredTreks" :key="trek.id" class="col-md-6 col-lg-4">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 h-100 overflow-hidden d-flex flex-column">
            <div class="p-4 flex-grow-1">
              <span class="badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-50 mb-3 px-3 py-2 rounded-pill">{{ getDifficultyStars(trek.difficulty) }} {{ trek.difficulty }}</span>
              <h3 class="h4 fw-bold text-light mb-2">{{ trek.name }}</h3>
              <p class="text-secondary text-truncate-2 mb-3" style="font-size: 0.95rem;">
                {{ trek.description || 'Embark on a unique trekking journey exploring pristine nature and scenic views.' }}
              </p>
              
              <div class="d-flex align-items-center gap-2 mb-2 text-secondary fs-6">
                <span><i class="bi bi-geo-alt-fill text-danger me-1"></i></span> <span>{{ trek.location }}</span>
              </div>
              <div class="d-flex align-items-center gap-2 mb-2 text-secondary fs-6">
                <span><i class="bi bi-calendar-event text-warning me-1"></i></span> <span>{{ trek.duration }} Days</span>
              </div>
              <div class="d-flex align-items-center gap-2 text-secondary fs-6">
                <span><i class="bi bi-people-fill text-info me-1"></i></span> <span class="text-info fw-bold">{{ trek.slots_left }} Slots Left</span>
              </div>
            </div>
            <div class="p-4 border-top border-secondary border-opacity-10 bg-black bg-opacity-10 mt-auto">
              <router-link :to="`/treks?id=${trek.id}`" class="btn btn-outline-secondary border-secondary text-light w-100 py-2 rounded-3">View Details</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Why Choose Us Section -->
    <div class="container my-5 py-4">
      <div class="text-center mb-5">
        <h2 class="display-5 fw-bold">Why Choose <span class="text-gradient">Us</span></h2>
        <p class="text-secondary">We deliver the ultimate adventure experiences safely and professionally</p>
      </div>
      <div class="row g-4">
        <!-- Item 1 -->
        <div class="col-md-6 col-lg-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100 text-center">
            <div class="fs-1 mb-3 text-info"><i class="bi bi-check-circle-fill"></i></div>
            <h4 class="h5 fw-bold mb-2 text-light">Certified Trek Leaders</h4>
            <p class="text-secondary mb-0 small">Every trek is guided by certified mountaineering professionals.</p>
          </div>
        </div>
        <!-- Item 2 -->
        <div class="col-md-6 col-lg-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100 text-center">
            <div class="fs-1 mb-3 text-info"><i class="bi bi-check-circle-fill"></i></div>
            <h4 class="h5 fw-bold mb-2 text-light">Safe Adventures</h4>
            <p class="text-secondary mb-0 small">Safety protocols, medical aid kits, and backup support on all trails.</p>
          </div>
        </div>
        <!-- Item 3 -->
        <div class="col-md-6 col-lg-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100 text-center">
            <div class="fs-1 mb-3 text-info"><i class="bi bi-check-circle-fill"></i></div>
            <h4 class="h5 fw-bold mb-2 text-light">Beautiful Destinations</h4>
            <p class="text-secondary mb-0 small">Handpicked scenic routes that display the best vistas in the mountains.</p>
          </div>
        </div>
        <!-- Item 4 -->
        <div class="col-md-6 col-lg-3">
          <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4 h-100 text-center">
            <div class="fs-1 mb-3 text-info"><i class="bi bi-check-circle-fill"></i></div>
            <h4 class="h5 fw-bold mb-2 text-light">Easy Online Booking</h4>
            <p class="text-secondary mb-0 small">Seamless scheduling, slot tracking, and instant role redirections.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- How It Works Section -->
    <div class="container my-5 py-4 text-center">
      <div class="mb-5">
        <h2 class="display-5 fw-bold">How It <span class="text-gradient">Works</span></h2>
        <p class="text-secondary">Your pathway from city life to mountain trails in 4 simple steps</p>
      </div>
      <div class="row g-4 position-relative">
        <div class="col-md-3">
          <div class="d-inline-flex align-items-center justify-content-center bg-info bg-opacity-10 border border-info border-opacity-25 text-info rounded-circle mb-3 shadow" style="width: 50px; height: 50px;">
            <strong class="fs-5">1</strong>
          </div>
          <h4 class="h5 fw-bold mb-2 text-light">Register</h4>
          <p class="text-secondary small mb-0">Create an account as a Trekker in seconds.</p>
        </div>
        <div class="col-md-3">
          <div class="d-inline-flex align-items-center justify-content-center bg-info bg-opacity-10 border border-info border-opacity-25 text-info rounded-circle mb-3 shadow" style="width: 50px; height: 50px;">
            <strong class="fs-5">2</strong>
          </div>
          <h4 class="h5 fw-bold mb-2 text-light">Choose Trek</h4>
          <p class="text-secondary small mb-0">Browse and search our curated list of open treks.</p>
        </div>
        <div class="col-md-3">
          <div class="d-inline-flex align-items-center justify-content-center bg-info bg-opacity-10 border border-info border-opacity-25 text-info rounded-circle mb-3 shadow" style="width: 50px; height: 50px;">
            <strong class="fs-5">3</strong>
          </div>
          <h4 class="h5 fw-bold mb-2 text-light">Book Trek</h4>
          <p class="text-secondary small mb-0">Secure your slots instantly online.</p>
        </div>
        <div class="col-md-3">
          <div class="d-inline-flex align-items-center justify-content-center bg-info bg-opacity-10 border border-info border-opacity-25 text-info rounded-circle mb-3 shadow" style="width: 50px; height: 50px;">
            <strong class="fs-5">4</strong>
          </div>
          <h4 class="h5 fw-bold mb-2 text-light">Join Adventure</h4>
          <p class="text-secondary small mb-0">Meet your group and begin your trekking journey.</p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="mt-5 pt-5 border-top border-secondary border-opacity-10 text-center text-secondary">
      <div class="container">
        <div class="row g-4 mb-4 text-start">
          <div class="col-md-6">
            <h5 class="text-light fw-bold mb-3"><img src="../assets/images/logo.png" alt="Logo" class="me-2" style="height: 24px; width: auto;" /> TrekSphere</h5>
            <p class="small text-secondary" style="max-width: 320px;">Empowering adventure seekers to discover and book remote wilderness routes safely.</p>
          </div>
          <div class="col-md-3">
            <h6 class="text-light fw-bold mb-3">Company</h6>
            <ul class="list-unstyled small gap-2 d-flex flex-column">
              <li><a href="#" class="text-secondary text-decoration-none hover-white">About Us</a></li>
              <li><a href="#" class="text-secondary text-decoration-none hover-white">Contact</a></li>
              <li><a href="#" class="text-secondary text-decoration-none hover-white">Terms & Services</a></li>
            </ul>
          </div>
          <div class="col-md-3">
            <h6 class="text-light fw-bold mb-3">Academic</h6>
            <p class="small text-secondary mb-0">Made for MAD-II Coursework</p>
            <p class="small text-secondary">V2 Single Page Application</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { publicService, authService } from '../services/api';

export default {
  name: 'Home',
  data() {
    return {
      stats: {
        total_treks: 25,
        total_trekkers: 180,
        total_staff: 8,
        total_bookings: 620
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
.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.hover-white:hover {
  color: var(--text-main) !important;
}
</style>
