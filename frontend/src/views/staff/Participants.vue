<template>
  <DashboardLayout role="staff">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Trek <span class="text-gradient">Participants</span></h1>
        <p class="text-secondary mb-0">Review registrations, manage attendance, or modify reservation status for your treks.</p>
      </div>
    </div>

    <!-- Search/Filters -->
    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 mb-4 shadow">
      <div class="row g-3">
        <div class="col-md-8">
          <div class="input-group">
            <span class="input-group-text bg-black bg-opacity-25 border-secondary text-secondary"><i class="bi bi-search"></i></span>
            <input 
              v-model="searchQuery" 
              @input="currentPage = 1" 
              type="text" 
              class="form-control bg-black bg-opacity-25 border-secondary text-light" 
              placeholder="Search by trekker name, email, or trek route..."
            />
          </div>
        </div>
        <div class="col-md-4">
          <select v-model="statusFilter" @change="currentPage = 1" class="form-select bg-black bg-opacity-25 border-secondary text-light">
            <option value="">All Statuses</option>
            <option value="Pending">Pending</option>
            <option value="Confirmed">Confirmed</option>
            <option value="Completed">Completed</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Participants Table Card -->
    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4">
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-info" role="status"></div>
      </div>

      <div v-else-if="filteredParticipants.length === 0" class="text-center py-5">
        <span class="display-4 text-secondary mb-3 d-block"><i class="bi bi-people-fill"></i></span>
        <p class="text-secondary mb-0">No registered participants found.</p>
      </div>

      <template v-else>
        <!-- ── DESKTOP TABLE (md+) ── -->
        <div class="d-none d-md-block table-responsive">
          <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
            <thead>
              <tr>
                <th class="text-secondary border-secondary">Trekker</th>
                <th class="text-secondary border-secondary">Trek Route</th>
                <th class="text-secondary border-secondary text-center">Slots Booked</th>
                <th class="text-secondary border-secondary">Booking Date</th>
                <th class="text-secondary border-secondary text-center">Status</th>
                <th class="text-secondary border-secondary text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in paginated" :key="p.booking_id">
                <td class="border-secondary border-opacity-10">
                  <div class="fw-bold text-light">{{ p.trekker_name }}</div>
                  <span class="text-secondary small">{{ p.email }}</span>
                </td>
                <td class="border-secondary border-opacity-10">
                  <div class="text-light fw-bold">{{ p.trek_name }}</div>
                </td>
                <td class="border-secondary border-opacity-10 text-center">
                  <span class="badge bg-secondary px-2 py-1">{{ p.slots }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-secondary small">{{ formatDate(p.booking_date) }}</td>
                <td class="border-secondary border-opacity-10 text-center">
                  <span class="badge" :class="getStatusClass(p.status)">{{ p.status }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-end">
                  <select 
                    :value="p.status" 
                    @change="updateBookingStatus(p.booking_id, $event.target.value)" 
                    class="form-select form-select-sm bg-dark text-light border-secondary py-1 px-2 d-inline-block w-auto rounded-3"
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

        <!-- ── MOBILE TABLE (< md): 3 columns + View button ── -->
        <div class="d-md-none table-responsive">
          <table class="table table-dark table-sm border-secondary border-opacity-10 align-middle">
            <thead>
              <tr>
                <th class="text-secondary border-secondary">Trekker</th>
                <th class="text-secondary border-secondary text-center">Status</th>
                <th class="text-secondary border-secondary text-end">Details</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in paginated" :key="p.booking_id">
                <td class="border-secondary border-opacity-10">
                  <div class="text-light small fw-bold text-truncate" style="max-width: 110px;">{{ p.trekker_name }}</div>
                  <span class="text-secondary text-truncate d-block" style="font-size: 0.7rem; max-width: 110px;">{{ p.trek_name }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-center">
                  <span class="badge" :class="getStatusClass(p.status)" style="font-size: 0.65rem; padding: 2px 6px;">{{ p.status }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-end">
                  <button @click="openDetail(p)" class="btn btn-outline-info btn-sm rounded-3 px-2 py-1">
                    <i class="bi bi-eye-fill"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ── PAGINATION (Show only if rows > 10) ── -->
        <div v-if="filteredParticipants.length > perPage" class="d-flex flex-wrap align-items-center justify-content-between gap-2 mt-3 pt-3 border-top border-secondary border-opacity-10">
          <small class="text-secondary">
            Showing {{ (currentPage - 1) * perPage + 1 }}–{{ Math.min(currentPage * perPage, filteredParticipants.length) }}
            of {{ filteredParticipants.length }} participants
          </small>
          <nav>
            <ul class="pagination pagination-sm mb-0 gap-1">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link border-secondary rounded-3" @click="currentPage--">
                  <i class="bi bi-chevron-left"></i>
                </button>
              </li>
              <li v-for="pageNum in totalPages" :key="pageNum" class="page-item" :class="{ active: pageNum === currentPage }">
                <button class="page-link border-secondary rounded-3"
                  :class="{ 'active-page': pageNum === currentPage }"
                  @click="currentPage = pageNum">{{ pageNum }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link border-secondary rounded-3" @click="currentPage++">
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
      <div v-if="detailParticipant" class="detail-backdrop" @click.self="detailParticipant = null">
        <div class="detail-sheet">
          <!-- Handle bar -->
          <div class="text-center mb-3"><div class="sheet-handle"></div></div>

          <div class="d-flex justify-content-between align-items-start mb-4">
            <div>
              <h5 class="text-light fw-bold mb-0">Trekker Details</h5>
              <small class="text-info fw-bold">Booking #{{ detailParticipant.booking_id }}</small>
            </div>
            <button class="btn-icon-close" @click="detailParticipant = null"><i class="bi bi-x-lg text-secondary"></i></button>
          </div>

          <div class="list-group list-group-flush mb-4">
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2">
              <span class="text-secondary small d-block mb-1">Trekker Name</span>
              <span class="text-light fw-bold">{{ detailParticipant.trekker_name }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2">
              <span class="text-secondary small d-block mb-1">Trekker Email</span>
              <span class="text-light text-break">{{ detailParticipant.email }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2">
              <span class="text-secondary small d-block mb-1">Assigned Trek Route</span>
              <span class="text-light fw-bold">{{ detailParticipant.trek_name }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between align-items-center">
              <span class="text-secondary small">Slots Booked</span>
              <span class="badge bg-secondary rounded-pill px-3 py-1">{{ detailParticipant.slots }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between align-items-center">
              <span class="text-secondary small">Booking Date</span>
              <span class="text-light small">{{ formatDate(detailParticipant.booking_date) }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between align-items-center">
              <span class="text-secondary small">Status</span>
              <span class="badge" :class="getStatusClass(detailParticipant.status)">{{ detailParticipant.status }}</span>
            </div>
          </div>

          <div class="mb-2">
            <label class="form-label text-secondary small">Change Reservation Status</label>
            <select 
              :value="detailParticipant.status" 
              @change="updateBookingStatus(detailParticipant.booking_id, $event.target.value); detailParticipant = null" 
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
import { staffService } from '../../services/api';
import { alertService } from '@/services/alert';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'StaffParticipants',
  components: {
    DashboardLayout
  },
  data() {
    return {
      participants: [],
      loading: true,
      searchQuery: '',
      statusFilter: '',
      currentPage: 1,
      perPage: 10,
      detailParticipant: null
    };
  },
  computed: {
    filteredParticipants() {
      return this.participants.filter(p => {
        // Status filter
        if (this.statusFilter && p.status !== this.statusFilter) return false;
        
        // Search filter
        if (this.searchQuery) {
          const q = this.searchQuery.toLowerCase();
          return (
            p.trekker_name.toLowerCase().includes(q) ||
            p.email.toLowerCase().includes(q) ||
            p.trek_name.toLowerCase().includes(q)
          );
        }
        return true;
      });
    },
    totalPages() {
      return Math.max(1, Math.ceil(this.filteredParticipants.length / this.perPage));
    },
    paginated() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filteredParticipants.slice(start, start + this.perPage);
    }
  },
  methods: {
    async fetchParticipants() {
      this.loading = true;
      try {
        const data = await staffService.getDashboardSummary();
        this.participants = data.participants;
      } catch (err) {
        console.error('Failed to load participants list', err);
      } finally {
        this.loading = false;
      }
    },
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
        case 'Confirmed': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Pending': return 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        case 'Completed': return 'bg-secondary bg-opacity-25 text-secondary border border-secondary border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    },
    async updateBookingStatus(bookingId, status) {
      try {
        await staffService.updateBookingStatus(bookingId, status);
        alertService.success('Booking status updated successfully!');
        this.fetchParticipants();
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Failed to update booking status.');
        this.fetchParticipants();
      }
    },
    openDetail(p) {
      this.detailParticipant = p;
    }
  },
  mounted() {
    this.fetchParticipants();
  }
}
</script>

<style scoped>
.page-link {
  min-width: 32px;
  text-align: center;
  background-color: rgba(30, 41, 59, 0.7) !important;
  color: #f8fafc !important;
  border-color: rgba(100, 116, 139, 0.3) !important;
  transition: all 0.2s;
}
.page-link:hover {
  background-color: rgba(0, 242, 254, 0.15) !important;
  color: #00f2fe !important;
  border-color: #00f2fe !important;
}
.page-item.disabled .page-link {
  background-color: rgba(15, 23, 42, 0.5) !important;
  color: #64748b !important;
  border-color: rgba(100, 116, 139, 0.1) !important;
  opacity: 0.5;
}
.page-link.active-page {
  background-color: #00f2fe !important;
  color: #0b0f19 !important;
  border-color: #00f2fe !important;
  font-weight: 700;
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
