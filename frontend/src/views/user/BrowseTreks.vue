<template>
  <DashboardLayout role="user">
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Browse <span class="text-gradient">Treks</span></h1>
        <p class="text-secondary mb-0">Search and filter active trekking trails, view dates, and reserve slots.</p>
      </div>
    </div>

    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 mb-5 shadow">
      <form @submit.prevent="fetchTreks" class="row g-3">
        <div class="col-md-4">
          <label class="form-label text-secondary small">Search Trails</label>
          <input 
            v-model="filters.search" 
            type="text" 
            class="form-control bg-black bg-opacity-25 border-secondary text-light py-2" 
            placeholder="Search by name, description..."
          />
        </div>
        <div class="col-md-3">
          <label class="form-label text-secondary small">Difficulty Level</label>
          <select v-model="filters.difficulty" class="form-select bg-black bg-opacity-25 border-secondary text-light py-2">
            <option value="">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
        <div class="col-md-3">
          <label class="form-label text-secondary small">Duration</label>
          <select v-model="filters.duration" class="form-select bg-black bg-opacity-25 border-secondary text-light py-2">
            <option value="">Any Duration</option>
            <option value="short">Short (1-3 days)</option>
            <option value="medium">Medium (4-7 days)</option>
            <option value="long">Long (8+ days)</option>
          </select>
        </div>
        <div class="col-md-2 d-flex align-items-end gap-2">
          <button type="button" @click="resetFilters" class="btn btn-outline-secondary border-secondary text-light w-50 py-2 rounded-3" title="Reset Filters">
            <i class="bi bi-arrow-counterclockwise"></i>
          </button>
          <button type="submit" class="btn btn-glow w-50 py-2 rounded-3" title="Search">
            <i class="bi bi-search"></i>
          </button>
        </div>
      </form>
    </div>


    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-info" role="status"></div>
    </div>

 
    <div v-else-if="treks.length === 0" class="text-center py-5 card bg-dark bg-opacity-25 border-secondary border-opacity-10 rounded-4 shadow">
      <span class="display-3 mb-2 d-block text-secondary"><i class="bi bi-compass"></i></span>
      <h3 class="h5 fw-bold text-light">No Treks Found</h3>
      <p class="text-secondary mb-0">Try adjusting your filters or search keywords.</p>
    </div>


    <div v-else class="row g-4">
      <div v-for="trek in treks" :key="trek.id" class="col-md-6 col-lg-4">
        <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 h-100 overflow-hidden d-flex flex-column hover-card">
          <div class="p-4 flex-grow-1">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <span class="badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-50 px-2 py-1 rounded-pill" :class="getDifficultyClass(trek.difficulty)">
                  {{ trek.difficulty }}
                </span>
                <span v-if="bookedTrekIds.includes(trek.id)" class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-50 px-2 py-1 rounded-pill ms-2">
                  Already Booked
                </span>
              </div>
              <span class="text-secondary small"><i class="bi bi-clock me-1 text-info"></i>{{ trek.duration }} Days</span>
            </div>
            
            <h5 class="fw-bold text-light mb-2">{{ trek.name }}</h5>
            <p class="text-secondary text-truncate-3 small mb-4">
              {{ trek.description || 'Embark on a unique trekking journey exploring pristine nature and scenic views.' }}
            </p>

            <div class="list-group list-group-flush small bg-transparent border-top border-secondary border-opacity-10 pt-3">
              <div class="d-flex justify-content-between mb-2">
                <span class="text-secondary"><i class="bi bi-geo-alt me-1 text-danger"></i>Location:</span>
                <span class="text-light fw-medium text-truncate text-end" style="max-width: 60%;">{{ trek.location }}</span>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span class="text-secondary"><i class="bi bi-calendar-event me-1 text-warning"></i>Departure:</span>
                <span class="text-light fw-medium">{{ formatDate(trek.start_date) }}</span>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span class="text-secondary"><i class="bi bi-people me-1 text-info"></i>Slots:</span>
                <span class="text-info fw-bold">{{ trek.slots_left }} / {{ trek.max_slots }} Available</span>
              </div>
              <div class="d-flex justify-content-between mb-2" v-if="trek.booking_close_time">
                <span class="text-secondary"><i class="bi bi-alarm me-1 text-warning"></i>Deadline:</span>
                <span :class="trek.booking_closed ? 'text-danger fw-bold' : 'text-warning fw-medium'">
                  {{ formatDateTime(trek.booking_close_time) }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="p-3 border-top border-secondary border-opacity-10 bg-black bg-opacity-10 d-flex gap-2">
            <button @click="showDetails(trek)" class="btn btn-outline-secondary border-secondary text-light w-100 py-2 rounded-3">
              View Details
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Trek Details Modal -->
    <div v-if="activeTrek" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); z-index: 1050;">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content card bg-dark border-secondary border-opacity-50 text-light shadow-lg rounded-4">
          <div class="modal-header border-bottom border-secondary border-opacity-15 p-4 d-flex justify-content-between align-items-center">
            <h4 class="modal-title fw-bold text-light mb-0">{{ activeTrek.name }}</h4>
            <button type="button" @click="closeDetails" class="btn-close btn-close-white" aria-label="Close"></button>
          </div>
          <div class="modal-body p-4">
            <div class="row g-4">
              <div class="col-md-7">
                <h6 class="text-gradient fw-bold uppercase-label mb-2">Trail Overview</h6>
                <p class="text-secondary small mb-4 pre-wrap" style="line-height: 1.6;">
                  {{ activeTrek.description || 'Embark on a unique trekking journey exploring pristine nature and scenic views.' }}
                </p>
                
                <div class="row g-3">
                  <div class="col-6 bg-black bg-opacity-20 border border-secondary border-opacity-10 rounded-3 p-3">
                    <span class="text-secondary tiny-text d-block">Start Location</span>
                    <strong class="text-light small"><i class="bi bi-geo-alt-fill text-danger me-1"></i>{{ activeTrek.location }}</strong>
                  </div>
                  <div class="col-6 bg-black bg-opacity-20 border border-secondary border-opacity-10 rounded-3 p-3">
                    <span class="text-secondary tiny-text d-block">Difficulty</span>
                    <strong class="text-light small"><i class="bi bi-award-fill text-warning me-1"></i>{{ activeTrek.difficulty }}</strong>
                  </div>
                  <div class="col-6 bg-black bg-opacity-20 border border-secondary border-opacity-10 rounded-3 p-3">
                    <span class="text-secondary tiny-text d-block">Starts</span>
                    <strong class="text-light small"><i class="bi bi-calendar-check-fill text-success me-1"></i>{{ formatDate(activeTrek.start_date) }}</strong>
                  </div>
                  <div class="col-6 bg-black bg-opacity-20 border border-secondary border-opacity-10 rounded-3 p-3">
                    <span class="text-secondary tiny-text d-block">Ends</span>
                    <strong class="text-light small"><i class="bi bi-calendar-x-fill text-secondary me-1"></i>{{ formatDate(activeTrek.end_date) }}</strong>
                  </div>
                </div>
              </div>


              <div class="col-md-5">
                <div class="p-4 rounded-4 bg-black bg-opacity-25 border border-secondary border-opacity-15 shadow-sm h-100 d-flex flex-column justify-content-between">
                  <div>
                    <h6 class="fw-bold text-light mb-3">Booking Information</h6>
                    
                    <div class="list-group list-group-flush bg-transparent small mb-4">
                      <div class="d-flex justify-content-between mb-2">
                        <span class="text-secondary">Duration</span>
                        <span class="text-light fw-bold">{{ activeTrek.duration }} Days</span>
                      </div>
                      <div class="d-flex justify-content-between mb-2">
                        <span class="text-secondary">Slots Available</span>
                        <span class="text-info fw-bold">{{ activeTrek.slots_left }} / {{ activeTrek.max_slots }}</span>
                      </div>
                      <div class="d-flex justify-content-between mb-2" v-if="activeTrek.booking_close_time">
                        <span class="text-secondary">Deadline</span>
                        <span :class="activeTrek.booking_closed ? 'text-danger fw-bold' : 'text-warning fw-bold'">
                          {{ formatDateTime(activeTrek.booking_close_time) }}
                        </span>
                      </div>
                    </div>
                  </div>


                  <div>
                    <div v-if="activeTrek.booking_closed" class="alert alert-danger bg-danger bg-opacity-10 border-danger border-opacity-20 text-danger text-center small rounded-3 p-3 mb-0">
                      <i class="bi bi-exclamation-triangle-fill me-2"></i>Booking Window Closed
                    </div>
                    <div v-else-if="activeTrek.slots_left <= 0" class="alert alert-warning bg-warning bg-opacity-10 border-warning border-opacity-20 text-warning text-center small rounded-3 p-3 mb-0">
                      <i class="bi bi-people-fill me-2"></i>Trek is Fully Booked
                    </div>
                    <div v-else>
                      <button v-if="bookedTrekIds.includes(activeTrek.id)" class="btn btn-secondary w-100 py-3 rounded-3 mt-2 cursor-not-allowed" disabled>
                        <i class="bi bi-check-circle-fill me-2"></i>Already Booked
                      </button>
                      <button v-else @click="confirmBooking" class="btn btn-glow w-100 py-3 rounded-3 mt-2" :disabled="submitting">
                        <span v-if="submitting" class="spinner-border spinner-border-sm me-1" role="status"></span>
                        Book Trek
                      </button>
                    </div>
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
import { publicService, userService } from '../../services/api';
import { alertService } from '@/services/alert';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'UserBrowseTreks',
  components: {
    DashboardLayout
  },
  data() {
    return {
      treks: [],
      loading: true,
      submitting: false,
      activeTrek: null,
      bookingSlots: 1,
      filters: {
        search: '',
        difficulty: '',
        duration: ''
      },
      bookedTrekIds: []
    };
  },
  methods: {
    async fetchTreks() {
      this.loading = true;
      try {
        const data = await publicService.getTreks(this.filters);
        // Only show Open status treks for general user browsing
        this.treks = data.filter(t => t.status === 'Open');
        
        try {
          const summary = await userService.getDashboardSummary();
          this.bookedTrekIds = summary.my_bookings.map(b => b.trek_id);
        } catch (e) {
          console.warn('Failed to load user bookings summary', e);
        }
      } catch (err) {
        alertService.error('Failed to load treks.');
      } finally {
        this.loading = false;
      }
    },
    resetFilters() {
      this.filters.search = '';
      this.filters.difficulty = '';
      this.filters.duration = '';
      this.fetchTreks();
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
    formatDateTime(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        const d = new Date(dateStr);
        return d.toLocaleString('en-GB', { 
          timeZone: 'Asia/Kolkata', 
          day: '2-digit',
          month: 'short',
          year: 'numeric', 
          hour: '2-digit', 
          minute: '2-digit',
          hour12: true
        });
      } catch (e) {
        return dateStr;
      }
    },
    getDifficultyClass(difficulty) {
      switch (difficulty) {
        case 'Easy': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Medium': return 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25';
        case 'Hard': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    },
    async showDetails(trek) {
      this.activeTrek = trek;
      this.bookingSlots = 1;
      
      // Fallback query parameter setting
      this.$router.replace({ path: '/browse-treks', query: { id: trek.id } });
    },
    closeDetails() {
      this.activeTrek = null;
      this.$router.replace({ path: '/browse-treks', query: {} });
    },
    async confirmBooking() {
      if (!this.activeTrek) return;
      this.submitting = true;
      try {
        await userService.createBooking(this.activeTrek.id, this.bookingSlots);
        alertService.success('Trek booking requested successfully!');
        this.closeDetails();
        this.fetchTreks();
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Failed to submit booking.');
      } finally {
        this.submitting = false;
      }
    }
  },
  mounted() {
    this.fetchTreks().then(() => {
      // Check query string parameters to open modal if id is passed
      const queryId = this.$route.query.id;
      if (queryId) {
        const matched = this.treks.find(t => t.id === parseInt(queryId));
        if (matched) {
          this.showDetails(matched);
        }
      }
    });
  }
}
</script>

<style scoped>
.hover-card {
  transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
}
.hover-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 242, 254, 0.4) !important;
  box-shadow: 0 10px 25px rgba(0, 242, 254, 0.1) !important;
}
.text-truncate-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.pre-wrap {
  white-space: pre-wrap;
}
.uppercase-label {
  font-size: 0.75rem;
  letter-spacing: 1px;
  text-transform: uppercase;
}
</style>
