<template>
  <DashboardLayout role="admin">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Manage <span class="text-gradient">Bookings</span></h1>
        <p class="text-secondary mb-0">Monitor trek reservations, issue tickets, and handle cancellations</p>
      </div>
    </div>

    <!-- Search & Filters -->
    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 mb-4 shadow">
      <div class="row g-3">
        <div class="col-md-8">
          <div class="input-group">
            <span class="input-group-text bg-black bg-opacity-25 border-secondary text-secondary"><i class="bi bi-search"></i></span>
            <input 
              v-model="filters.search" 
              @input="onFilterChange" 
              type="text" 
              class="form-control bg-black bg-opacity-25 border-secondary text-light" 
              placeholder="Search by trekker name or trek destination..."
            />
          </div>
        </div>
        <div class="col-md-4">
          <select v-model="filters.status" @change="onFilterChange" class="form-select bg-black bg-opacity-25 border-secondary text-light">
            <option value="">All Reservation Statuses</option>
            <option value="Pending">Pending</option>
            <option value="Confirmed">Confirmed</option>
            <option value="Cancelled">Cancelled</option>
            <option value="Completed">Completed</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Bookings Table Card -->
    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4">
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-info" role="status"></div>
      </div>

      <div v-else-if="bookings.length === 0" class="text-center py-5">
        <span class="display-4 text-secondary mb-3 d-block"><i class="bi bi-receipt-cutoff"></i></span>
        <p class="text-secondary mb-0">No booking records found.</p>
      </div>

      <template v-else>
        <!-- ── DESKTOP TABLE (md+) ── -->
        <div class="d-none d-md-block table-responsive">
          <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
            <thead>
              <tr>
                <th class="text-secondary border-secondary">Booking ID</th>
                <th class="text-secondary border-secondary">Trekker</th>
                <th class="text-secondary border-secondary">Trek</th>
                <th class="text-secondary border-secondary text-center">Slots Booked</th>
                <th class="text-secondary border-secondary">Booking Date</th>
                <th class="text-secondary border-secondary text-center">Status</th>
                <th class="text-secondary border-secondary text-end">Modify Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in paginated" :key="b.id">
                <td class="border-secondary border-opacity-10 text-info fw-bold">#{{ b.id }}</td>
                <td class="border-secondary border-opacity-10">
                  <div class="fw-bold text-light">{{ b.user_name }}</div>
                  <span class="text-secondary small">{{ b.user_email }}</span>
                </td>
                <td class="border-secondary border-opacity-10">
                  <div class="text-light fw-bold">{{ b.trek_name }}</div>
                  <span class="text-secondary small">📍 {{ b.trek_location }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-center text-secondary">
                  <span class="badge bg-secondary px-2 py-1">{{ b.slots_booked }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-secondary small">{{ formatDate(b.booking_date) }}</td>
                <td class="border-secondary border-opacity-10 text-center">
                  <span class="badge" :class="getStatusClass(b.status)">{{ b.status }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-end">
                  <select 
                    :value="b.status" 
                    @change="updateStatus(b.id, $event.target.value)" 
                    class="form-select form-select-sm bg-dark text-light border-secondary py-1 px-2 d-inline-block w-auto"
                  >
                    <option value="Pending">Pending</option>
                    <option value="Confirmed">Confirmed</option>
                    <option value="Cancelled">Cancelled</option>
                    <option value="Completed">Completed</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ── MOBILE TABLE (< md): 3 columns + View Button ── -->
        <div class="d-md-none table-responsive">
          <table class="table table-dark table-sm border-secondary border-opacity-10 align-middle">
            <thead>
              <tr>
                <th class="text-secondary border-secondary">Trekker</th>
                <th class="text-secondary border-secondary">Trek</th>
                <th class="text-secondary border-secondary text-end">Details</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in paginated" :key="b.id">
                <td class="border-secondary border-opacity-10">
                  <div class="text-light small fw-bold text-truncate" style="max-width: 100px;">{{ b.user_name }}</div>
                  <span class="badge" :class="getStatusClass(b.status)" style="font-size: 0.65rem; padding: 2px 6px;">{{ b.status }}</span>
                </td>
                <td class="border-secondary border-opacity-10">
                  <div class="text-secondary small text-truncate" style="max-width: 120px;" :title="b.trek_name">{{ b.trek_name }}</div>
                  <span class="text-muted" style="font-size: 0.7rem;">Slots: {{ b.slots_booked }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-end">
                  <button @click="openDetail(b)" class="btn btn-outline-info btn-sm rounded-3 px-2 py-1">
                    <i class="bi bi-eye-fill"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ── PAGINATION ── -->
        <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mt-3 pt-3 border-top border-secondary border-opacity-10">
          <small class="text-secondary">
            Showing {{ (currentPage - 1) * perPage + 1 }}–{{ Math.min(currentPage * perPage, bookings.length) }}
            of {{ bookings.length }} bookings
          </small>
          <nav>
            <ul class="pagination pagination-sm mb-0 gap-1">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link bg-dark border-secondary text-secondary rounded-3" @click="currentPage--">
                  <i class="bi bi-chevron-left"></i>
                </button>
              </li>
              <li v-for="p in totalPages" :key="p" class="page-item" :class="{ active: p === currentPage }">
                <button class="page-link bg-dark border-secondary text-secondary rounded-3"
                  :class="{ 'bg-info border-info text-dark': p === currentPage }"
                  @click="currentPage = p">{{ p }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link bg-dark border-secondary text-secondary rounded-3" @click="currentPage++">
                  <i class="bi bi-chevron-right"></i>
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </template>
    </div>

    <!-- ── MOBILE DETAIL BOTTOM-SHEET MODAL ── -->
    <Teleport to="body">
      <div v-if="detailBooking" class="detail-backdrop" @click.self="detailBooking = null">
        <div class="detail-sheet">
          <!-- Handle bar -->
          <div class="text-center mb-3"><div class="sheet-handle"></div></div>

          <div class="d-flex justify-content-between align-items-start mb-4">
            <div>
              <h5 class="text-light fw-bold mb-0">Booking Details</h5>
              <small class="text-info fw-bold">#{{ detailBooking.id }}</small>
            </div>
            <button class="btn-icon-close" @click="detailBooking = null"><i class="bi bi-x-lg text-secondary"></i></button>
          </div>

          <div class="list-group list-group-flush mb-4">
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2">
              <span class="text-secondary small d-block mb-1">Trekker Name</span>
              <span class="text-light fw-bold">{{ detailBooking.user_name }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2">
              <span class="text-secondary small d-block mb-1">Trekker Email</span>
              <span class="text-light text-break">{{ detailBooking.user_email }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2">
              <span class="text-secondary small d-block mb-1">Trek</span>
              <span class="text-light fw-bold">{{ detailBooking.trek_name }}</span>
              <span class="text-secondary small d-block">📍 {{ detailBooking.trek_location }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between align-items-center">
              <span class="text-secondary small">Slots Booked</span>
              <span class="badge bg-secondary rounded-pill px-3 py-1">{{ detailBooking.slots_booked }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between align-items-center">
              <span class="text-secondary small">Booking Date</span>
              <span class="text-light small">{{ formatDate(detailBooking.booking_date) }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between align-items-center">
              <span class="text-secondary small">Status</span>
              <span class="badge" :class="getStatusClass(detailBooking.status)">{{ detailBooking.status }}</span>
            </div>
          </div>

          <div class="mb-2">
            <label class="form-label text-secondary small">Change Reservation Status</label>
            <select 
              :value="detailBooking.status" 
              @change="updateStatus(detailBooking.id, $event.target.value); detailBooking = null" 
              class="form-select bg-dark text-light border-secondary py-2 px-3 rounded-3"
            >
              <option value="Pending">Pending</option>
              <option value="Confirmed">Confirmed</option>
              <option value="Cancelled">Cancelled</option>
              <option value="Completed">Completed</option>
            </select>
          </div>
        </div>
      </div>
    </Teleport>
  </DashboardLayout>
</template>

<script>
import { adminService } from '../../services/api';
import { alertService } from '@/services/alert';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'AdminBookings',
  components: {
    DashboardLayout
  },
  data() {
    return {
      bookings: [],
      loading: true,
      detailBooking: null,
      currentPage: 1,
      perPage: 10,
      filters: {
        search: '',
        status: ''
      }
    };
  },
  computed: {
    totalPages() {
      return Math.max(1, Math.ceil(this.bookings.length / this.perPage));
    },
    paginated() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.bookings.slice(start, start + this.perPage);
    }
  },
  methods: {
    async fetchBookings() {
      this.loading = true;
      try {
        const data = await adminService.getBookings({
          search: this.filters.search,
          status: this.filters.status
        });
        this.bookings = data;
      } catch (err) {
        console.error('Failed to load bookings log', err);
      } finally {
        this.loading = false;
      }
    },
    onFilterChange() {
      this.currentPage = 1;
      this.fetchBookings();
    },
    openDetail(booking) {
      this.detailBooking = booking;
    },
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
    async updateStatus(bookingId, status) {
      try {
        await adminService.updateBookingStatus(bookingId, status);
        alertService.success('Booking status updated successfully!');
        this.fetchBookings();
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Failed to update booking status.');
        this.fetchBookings();
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 'Confirmed': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Pending': return 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        case 'Completed': return 'bg-secondary bg-opacity-25 text-secondary border border-secondary border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    }
  },
  mounted() {
    this.fetchBookings();
  }
}
</script>

<style scoped>
.page-link {
  min-width: 32px;
  text-align: center;
}

/* Detail bottom-sheet modal */
.detail-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1060;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.detail-sheet {
  width: 100%;
  max-width: 540px;
  background: #0d1117;
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 20px 20px 0 0;
  padding: 16px 20px 32px;
  animation: slideUp 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.sheet-handle {
  width: 40px;
  height: 4px;
  background: rgba(100, 116, 139, 0.4);
  border-radius: 2px;
  margin: 0 auto;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.btn-icon-close {
  background: none;
  border: none;
  padding: 6px;
  border-radius: 8px;
  cursor: pointer;
}
</style>
