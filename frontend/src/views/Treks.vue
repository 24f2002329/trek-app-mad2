<template>
  <div class="container py-5">
    <div class="row mb-5">
      <div class="col-10 mx-auto text-center">
        <h1 class="display-5 fw-bold">Explore <span class="text-gradient">Trekking Trails</span></h1>
        <p class="text-secondary">Find your next journey from our catalog of open treks</p>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="card bg-dark bg-opacity-70 border-secondary border-opacity-25 shadow rounded-4 p-4 mb-5">
      <form @submit.prevent="fetchTreks" class="row g-2 align-items-center">
        <div class="col-md-9">
          <input v-model="filters.search" type="text" class="form-control bg-dark text-light border-secondary py-3 px-4 rounded-3" placeholder="Search treks by name, location, or difficulty (e.g. Hampta, Easy, Uttarakhand)..." />
        </div>
        <div class="col-md-3 d-flex gap-2">
          <button type="button" @click="resetFilters" class="btn btn-outline-secondary border-secondary text-light flex-grow-1 py-3 rounded-3">Reset</button>
          <button type="submit" class="btn btn-glow flex-grow-1 py-3 rounded-3">Search</button>
        </div>
      </form>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-info" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="treks.length === 0" class="text-center py-5 card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 shadow">
      <span class="display-3 mb-3 d-block text-secondary"><i class="bi bi-search"></i></span>
      <h3 class="h4 fw-bold text-light">No Treks Found</h3>
      <p class="text-secondary">Try adjusting your filters or search keywords.</p>
    </div>

    <!-- Treks Grid -->
    <div v-else class="row g-4">
      <div v-for="trek in treks" :key="trek.id" class="col-md-6 col-lg-4">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 h-100 overflow-hidden d-flex flex-column" :class="{ 'border-info': selectedTrekId === trek.id }">
          <div class="p-4 flex-grow-1">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <span class="badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-50 px-3 py-2 rounded-pill">{{ getDifficultyStars(trek.difficulty) }} {{ trek.difficulty }}</span>
              <span class="text-secondary small">⏳ {{ trek.duration }} Days</span>
            </div>
            <h3 class="h4 fw-bold text-light mb-2">{{ trek.name }}</h3>
            <p class="text-secondary text-truncate-3 mb-4" style="font-size: 0.95rem;">
              {{ trek.description || 'Embark on a unique trekking journey exploring pristine nature and scenic views.' }}
            </p>
            
            <div class="row g-2 pt-2 border-top border-secondary border-opacity-10 text-secondary small">
              <div class="col-6 mb-1">
                <span><i class="bi bi-geo-alt-fill text-danger me-1"></i> Location:</span>
                <div class="text-light fw-medium text-truncate">{{ trek.location }}</div>
              </div>
              <div class="col-6 mb-1">
                <span><i class="bi bi-calendar-event text-warning me-1"></i> Starts:</span>
                <div class="text-light fw-medium">{{ formatDate(trek.start_date) }}</div>
              </div>
              <div class="col-6">
                <span><i class="bi bi-people-fill text-info me-1"></i> Available Slots:</span>
                <div class="text-info fw-bold">{{ trek.slots_left }} / {{ trek.max_slots }}</div>
              </div>
            </div>
          </div>
          <div class="p-4 border-top border-secondary border-opacity-10 bg-black bg-opacity-10 d-flex gap-2">
            <button @click="showDetails(trek)" class="btn btn-outline-secondary border-secondary text-light flex-grow-1 py-2 rounded-3">View Details</button>
            <button @click="bookNow(trek)" class="btn btn-glow px-4 py-2">Book Now</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="activeTrek" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.85); backdrop-filter: blur(8px);">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content card bg-dark border-secondary border-opacity-50 text-light shadow-lg">
          <div class="modal-header border-bottom border-secondary border-opacity-10 p-4">
            <h4 class="modal-title fw-bold text-light">{{ activeTrek.name }}</h4>
            <button type="button" @click="closeDetails" class="btn-close btn-close-white" aria-label="Close"></button>
          </div>
          <div class="modal-body p-4">
            <div class="row g-4">
              <div class="col-md-8">
                <h5 class="fw-bold text-gradient mb-3">Trek Description</h5>
                <p class="text-secondary mb-4" style="white-space: pre-line; line-height: 1.6;">
                  {{ activeTrek.description || 'Embark on a unique trekking journey exploring pristine nature and scenic views. This trail offers amazing views of mountain ridges, custom photography points, and unique local flora.' }}
                </p>
                
                <h5 class="fw-bold text-gradient mb-3">Itinerary Details</h5>
                <div class="d-flex flex-column gap-3">
                  <div class="d-flex align-items-center gap-3">
                    <span class="fs-4 text-info"><i class="bi bi-geo-alt"></i></span>
                    <div>
                      <strong class="d-block text-light">Region / Location</strong>
                      <span class="text-secondary small">{{ activeTrek.location }}</span>
                    </div>
                  </div>
                  <div class="d-flex align-items-center gap-3">
                    <span class="fs-4 text-info"><i class="bi bi-hourglass-split"></i></span>
                    <div>
                      <strong class="d-block text-light">Duration</strong>
                      <span class="text-secondary small">{{ activeTrek.duration }} Days of guided expedition</span>
                    </div>
                  </div>
                  <div class="d-flex align-items-center gap-3">
                    <span class="fs-4 text-info"><i class="bi bi-calendar-range"></i></span>
                    <div>
                      <strong class="d-block text-light">Dates</strong>
                      <span class="text-secondary small">{{ formatDate(activeTrek.start_date) }} to {{ formatDate(activeTrek.end_date) }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="p-3 rounded-3 bg-black bg-opacity-20 border border-secondary border-opacity-20">
                  <h6 class="fw-bold mb-3 text-light">Trek Overview</h6>
                  <div class="d-flex flex-column gap-2 small mb-4">
                    <div class="d-flex justify-content-between">
                      <span class="text-secondary">Difficulty:</span>
                      <span class="text-light fw-bold">{{ activeTrek.difficulty }}</span>
                    </div>
                    <div class="d-flex justify-content-between">
                      <span class="text-secondary">Max Slots:</span>
                      <span class="text-light fw-bold">{{ activeTrek.max_slots }}</span>
                    </div>
                    <div class="d-flex justify-content-between">
                      <span class="text-secondary">Available Slots:</span>
                      <span class="text-info fw-bold">{{ activeTrek.slots_left }}</span>
                    </div>
                    <div class="d-flex justify-content-between" v-if="activeTrek.assigned_staff">
                      <span class="text-secondary">Leader:</span>
                      <span class="text-light fw-bold">{{ activeTrek.assigned_staff.name }}</span>
                    </div>
                  </div>

                  <!-- Booking Widget Inside Details -->
                  <div v-if="isTrekker">
                    <h6 class="fw-bold mb-2 text-light">Book Slots</h6>
                    <div class="input-group mb-3">
                      <button class="btn btn-outline-secondary border-secondary text-light px-2 py-1" type="button" @click="bookingSlots = Math.max(1, bookingSlots - 1)">-</button>
                      <input type="number" v-model.number="bookingSlots" class="form-control bg-dark text-light border-secondary text-center" min="1" :max="activeTrek.slots_left" />
                      <button class="btn btn-outline-secondary border-secondary text-light px-2 py-1" type="button" @click="bookingSlots = Math.min(activeTrek.slots_left, bookingSlots + 1)">+</button>
                    </div>
                    <button @click="confirmBooking" class="btn btn-glow w-100 py-2 rounded-3" :disabled="activeTrek.slots_left <= 0">
                      {{ activeTrek.slots_left <= 0 ? 'Fully Booked' : 'Confirm Booking' }}
                    </button>
                  </div>
                  <div v-else-if="!isLoggedIn">
                    <button @click="redirectToLogin" class="btn btn-glow w-100 py-2 rounded-3">Log In to Book</button>
                  </div>
                  <div v-else class="text-center py-2 text-warning small border-top border-secondary border-opacity-10">
                    Booking is only available for trekkers.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Modal/Toast -->
    <div v-if="successMessage" class="position-fixed bottom-0 end-0 p-3" style="z-index: 1060;">
      <div class="toast show card bg-dark border-info text-light" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header bg-dark text-info border-bottom border-secondary border-opacity-10 d-flex justify-content-between">
          <strong class="me-auto"><i class="bi bi-check-circle-fill text-success me-2"></i> Booking Status</strong>
          <button type="button" @click="successMessage = ''" class="btn-close btn-close-white" aria-label="Close"></button>
        </div>
        <div class="toast-body p-3">
          {{ successMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { publicService, userService, authService } from '../services/api';

export default {
  name: 'Treks',
  data() {
    return {
      treks: [],
      filters: {
        search: '',
        location: '',
        difficulty: ''
      },
      loading: true,
      activeTrek: null,
      selectedTrekId: null,
      bookingSlots: 1,
      isLoggedIn: false,
      isTrekker: false,
      successMessage: ''
    };
  },
  methods: {
    getDifficultyStars(difficulty) {
      const diff = (difficulty || '').toLowerCase();
      if (diff.includes('easy')) return '⭐';
      if (diff.includes('moderate')) return '⭐⭐';
      if (diff.includes('hard') || diff.includes('difficult')) return '⭐⭐⭐';
      return '⭐';
    },
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      } catch (e) {
        return dateStr;
      }
    },
    async fetchTreks() {
      this.loading = true;
      try {
        const treksList = await publicService.getTreks({
          search: this.filters.search,
          location: this.filters.location,
          difficulty: this.filters.difficulty
        });
        this.treks = treksList;
        
        // If route query contains trek id, auto-open details
        const queryTrekId = this.$route.query.id;
        if (queryTrekId) {
          const matched = this.treks.find(t => t.id === parseInt(queryTrekId));
          if (matched) {
            this.showDetails(matched);
          }
        }
      } catch (err) {
        console.error('Failed to load treks list', err);
      } finally {
        this.loading = false;
      }
    },
    resetFilters() {
      this.filters.search = '';
      this.filters.location = '';
      this.filters.difficulty = '';
      this.fetchTreks();
    },
    async showDetails(trek) {
      this.selectedTrekId = trek.id;
      this.bookingSlots = 1;
      try {
        const detailedTrek = await publicService.getTrekDetail(trek.id);
        this.activeTrek = detailedTrek;
      } catch (err) {
        console.warn('Failed to fetch detailed trek info, fallback to list item', err);
        this.activeTrek = trek;
      }
    },
    closeDetails() {
      this.activeTrek = null;
      this.selectedTrekId = null;
      this.$router.replace({ path: '/treks', query: {} });
    },
    bookNow(trek) {
      this.selectedTrekId = trek.id;
      if (!this.isLoggedIn) {
        this.redirectToLogin();
      } else if (!this.isTrekker) {
        alert('Booking is only available for accounts registered as Trekkers.');
      } else {
        this.showDetails(trek);
      }
    },
    redirectToLogin() {
      this.$router.push({
        path: '/login',
        query: { redirect: `/treks?id=${this.selectedTrekId || ''}` }
      });
    },
    async confirmBooking() {
      if (!this.activeTrek) return;
      try {
        const response = await userService.createBooking(this.activeTrek.id, this.bookingSlots);
        this.successMessage = response.message || 'Booking request submitted!';
        this.closeDetails();
        this.fetchTreks();
        
        setTimeout(() => {
          this.successMessage = '';
        }, 4000);
      } catch (err) {
        const errMsg = err.response?.data?.message || 'Failed to submit booking request.';
        alert(errMsg);
      }
    }
  },
  mounted() {
    this.isLoggedIn = authService.isAuthenticated();
    const user = authService.getCurrentUser();
    this.isTrekker = user && user.role === 'trekker';
    this.fetchTreks();
  }
}
</script>

<style scoped>
.text-truncate-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
