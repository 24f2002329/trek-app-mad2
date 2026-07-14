<template>
  <DashboardLayout role="user">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-md-6 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">My <span class="text-gradient">Bookings</span></h1>
        <p class="text-secondary mb-0">Manage your active reservations, check approval status, or cancel bookings.</p>
      </div>
      <div class="col-md-6 text-center text-md-end mt-3 mt-md-0">
        <router-link to="/browse-treks" class="btn btn-glow px-4 py-2">
          <i class="bi bi-compass me-1"></i>Find New Trek
        </router-link>
      </div>
    </div>

    <!-- Bookings Container -->
    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow">
      <h5 class="fw-bold text-light mb-4">Active Reserves</h5>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-info" role="status"></div>
      </div>

      <!-- Empty State -->
      <div v-else-if="activeBookings.length === 0" class="text-center py-5">
        <span class="display-3 mb-2 d-block text-secondary"><i class="bi bi-calendar-x"></i></span>
        <p class="text-secondary">You do not have any active bookings at the moment.</p>
        <router-link to="/browse-treks" class="btn btn-outline-secondary border-secondary text-light btn-sm px-3 rounded-3 mt-2">
          Browse Trails
        </router-link>
      </div>

      <!-- Bookings Table -->
      <div v-else class="table-responsive">
        <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
          <thead>
            <tr>
              <th class="text-secondary border-secondary">Destination Details</th>
              <th class="text-secondary border-secondary">Reserved On</th>
              <th class="text-secondary border-secondary text-center">Slots Booked</th>
              <th class="text-secondary border-secondary">Status</th>
              <th class="text-secondary border-secondary text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in activeBookings" :key="b.booking_id">
              <td class="border-secondary border-opacity-10">
                <div class="fw-bold text-light fs-6">{{ b.trek_name }}</div>
                <span class="small text-secondary d-block mt-1">
                  📍 {{ b.location }} | 📅 Starts: {{ formatDate(b.start_date) }} | ⏳ {{ b.duration }} Days
                </span>
              </td>
              <td class="small text-secondary border-secondary border-opacity-10">
                {{ formatDate(b.booking_date) }}
              </td>
              <td class="border-secondary border-opacity-10 text-center text-info fw-bold">
                {{ b.slots }}
              </td>
              <td class="border-secondary border-opacity-10">
                <span class="badge rounded-pill" :class="getStatusClass(b.status)">{{ b.status }}</span>
              </td>
              <td class="border-secondary border-opacity-10 text-end">
                <button 
                  @click="cancelBooking(b)" 
                  class="btn btn-outline-danger btn-sm rounded-3 px-3 py-2 fw-semibold"
                  :disabled="cancellingId === b.booking_id"
                >
                  <span v-if="cancellingId === b.booking_id" class="spinner-border spinner-border-sm me-1" role="status"></span>
                  <i class="bi bi-x-circle me-1"></i>Cancel
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import { userService } from '../../services/api';
import { alertService } from '@/services/alert';
import { confirmService } from '@/services/confirm';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'UserBookings',
  components: {
    DashboardLayout
  },
  data() {
    return {
      activeBookings: [],
      loading: true,
      cancellingId: null
    };
  },
  methods: {
    async fetchBookings() {
      this.loading = true;
      try {
        const data = await userService.getDashboardSummary();
        // Filter out completed and cancelled bookings
        this.activeBookings = data.my_bookings.filter(
          b => b.status === 'Booked'
        );
      } catch (err) {
        alertService.error('Failed to load active bookings.');
      } finally {
        this.loading = false;
      }
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
    getStatusClass(status) {
      switch (status) {
        case 'Booked': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        case 'Completed': return 'bg-secondary bg-opacity-25 text-secondary border border-secondary border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    },
    async cancelBooking(booking) {
      const msg = `Are you sure you want to cancel your reservation for "${booking.trek_name}"?\nWarning: This releases all ${booking.slots} reserved slot(s) back to the trek.`;
      const confirmed = await confirmService.ask(msg, {
        title: 'Cancel Reservation',
        confirmText: 'Cancel Booking',
        isDanger: true
      });
      
      if (confirmed) {
        this.cancellingId = booking.booking_id;
        try {
          await userService.cancelBooking(booking.booking_id);
          alertService.success('Reservation cancelled successfully.');
          await this.fetchBookings();
        } catch (err) {
          alertService.error(err.response?.data?.message || 'Failed to cancel reservation.');
        } finally {
          this.cancellingId = null;
        }
      }
    }
  },
  mounted() {
    this.fetchBookings();
  }
}
</script>
