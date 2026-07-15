<template>
  <DashboardLayout role="user">
    <div class="row align-items-center mb-5">
      <div class="col-md-6 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Trek <span class="text-gradient">History</span></h1>
        <p class="text-secondary mb-0">Review your past journeys, completed adventures, and cancelled registrations.</p>
      </div>
      <div class="col-md-6 text-center text-md-end mt-3 mt-md-0 d-flex justify-content-md-end gap-2 flex-wrap justify-content-center">
        <button @click="triggerCSVExport" :disabled="exporting" class="btn btn-outline-info px-4 py-2 rounded-3">
          <span v-if="exporting">
            <span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
            Exporting...
          </span>
          <span v-else>
            <i class="bi bi-file-earmark-arrow-down me-1"></i>Export History
          </span>
        </button>
      </div>
    </div>


    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 shadow">
      <h5 class="fw-bold text-light mb-4">Past Trails</h5>


      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-info" role="status"></div>
      </div>

 
      <div v-else-if="history.length === 0" class="text-center py-5">
        <span class="display-3 mb-2 d-block text-secondary"><i class="bi bi-clock-history"></i></span>
        <p class="text-secondary">No trek history found.</p>
      </div>

      <template v-else>
        <!-- History Table — DESKTOP -->
        <div class="d-none d-md-block table-responsive">
          <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
            <thead>
              <tr>
                <th class="text-secondary border-secondary">Trek</th>
                <th class="text-secondary border-secondary">Reserved On</th>
                <th class="text-secondary border-secondary text-center">Slots</th>
                <th class="text-secondary border-secondary">Outcome</th>
                <th class="text-secondary border-secondary text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in history" :key="b.booking_id">
                <td class="border-secondary border-opacity-10">
                  <div @click="openTrekDetails(b.trek_id)" class="fw-bold text-light fs-6 cursor-pointer hover-text-info">{{ b.trek_name }}</div>
                  <span class="small text-secondary d-block mt-1">
                    <i class="bi bi-geo-alt me-1 text-danger"></i>{{ b.location }} | <i class="bi bi-clock me-1 text-warning"></i>{{ b.duration }} Days | <i class="bi bi-calendar-event me-1 text-info"></i>Started: {{ formatDate(b.start_date) }}
                  </span>
                </td>
                <td class="small text-secondary border-secondary border-opacity-10">
                  {{ formatDate(b.booking_date) }}
                </td>
                <td class="border-secondary border-opacity-10 text-center text-secondary">
                  {{ b.slots }}
                </td>
                <td class="border-secondary border-opacity-10">
                  <span class="badge rounded-pill" :class="getStatusClass(b.status)">{{ getOutcomeLabel(b) }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-end">
                  <button 
                    @click="openTrekDetails(b.trek_id)" 
                    class="btn btn-outline-info btn-sm rounded-3 px-3 py-2 fw-semibold"
                    :disabled="loadingDetailsId === b.trek_id"
                  >
                    <span v-if="loadingDetailsId === b.trek_id" class="spinner-border spinner-border-sm me-1" role="status"></span>
                    <i class="bi bi-info-circle me-1"></i>Trek Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- History Table — MOBILE -->
        <div class="d-md-none table-responsive">
          <table class="table table-dark table-sm border-secondary border-opacity-10 align-middle">
            <thead>
              <tr>
                <th class="text-secondary border-secondary">Trek</th>
                <th class="text-secondary border-secondary text-center">Outcome</th>
                <th class="text-secondary border-secondary text-end">Details</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in history" :key="b.booking_id">
                <td class="border-secondary border-opacity-10">
                  <div class="text-light small fw-bold text-truncate" style="max-width: 130px;">{{ b.trek_name }}</div>
                  <span class="text-secondary text-truncate d-block" style="font-size: 0.7rem; max-width: 130px;">
                    <i class="bi bi-geo-alt me-1 text-danger"></i>{{ b.location }}
                  </span>
                </td>
                <td class="border-secondary border-opacity-10 text-center">
                  <span class="badge rounded-pill" :class="getStatusClass(b.status)" style="font-size: 0.65rem; padding: 2px 6px;">{{ getOutcomeLabel(b) }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-end">
                  <button @click="mobileDetail = b" class="btn btn-outline-info btn-sm rounded-3 px-2 py-1">
                    <i class="bi bi-eye-fill"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>

    <!-- Mobile History Detail Bottom-Sheet -->
    <Teleport to="body">
      <div v-if="mobileDetail" class="detail-backdrop" @click.self="mobileDetail = null">
        <div class="detail-sheet">
          <div class="text-center mb-3"><div class="sheet-handle"></div></div>
          <div class="d-flex justify-content-between align-items-start mb-3">
            <div>
              <h5 class="text-light fw-bold mb-0">{{ mobileDetail.trek_name }}</h5>
              <small class="text-secondary"><i class="bi bi-geo-alt me-1 text-danger"></i>{{ mobileDetail.location }}</small>
            </div>
            <button class="btn-icon-close" @click="mobileDetail = null"><i class="bi bi-x-lg text-secondary"></i></button>
          </div>
          <div class="list-group list-group-flush mb-3">
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between">
              <span class="text-secondary small">Started</span>
              <span class="text-light small">{{ formatDate(mobileDetail.start_date) }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between">
              <span class="text-secondary small">Duration</span>
              <span class="text-light small">{{ mobileDetail.duration }} Days</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between">
              <span class="text-secondary small">Reserved On</span>
              <span class="text-light small">{{ formatDate(mobileDetail.booking_date) }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between">
              <span class="text-secondary small">Slots</span>
              <span class="badge bg-secondary rounded-pill px-3">{{ mobileDetail.slots }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-2 d-flex justify-content-between">
              <span class="text-secondary small">Outcome</span>
              <span class="badge rounded-pill" :class="getStatusClass(mobileDetail.status)">{{ getOutcomeLabel(mobileDetail) }}</span>
            </div>
          </div>
          <button @click="openTrekDetails(mobileDetail.trek_id); mobileDetail = null" class="btn btn-outline-info w-100 rounded-3 py-2" :disabled="loadingDetailsId === mobileDetail.trek_id">
            <i class="bi bi-info-circle me-1"></i>Trek & Guide Details
          </button>
        </div>
      </div>
    </Teleport>

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
                <h6 class="text-gradient fw-bold uppercase-label mb-2">Trail Overview / Notes</h6>
                <p class="text-secondary small mb-4 pre-wrap" style="line-height: 1.6;">
                  {{ activeTrek.description || 'Embark on a unique trekking journey exploring pristine nature and scenic views.' }}
                </p>
                
                <div class="row g-3 mb-2">
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
                <div class="p-4 rounded-4 bg-black bg-opacity-25 border border-secondary border-opacity-15 shadow-sm h-100 d-flex flex-column">
                  <h6 class="text-gradient fw-bold uppercase-label mb-3">Assigned Guide Info</h6>
                  
                  <div v-if="activeTrek.assigned_staff">
                    <div class="d-flex align-items-center mb-3">
                      <div class="bg-info bg-opacity-10 text-info rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 48px; height: 48px;">
                        <i class="bi bi-person-badge fs-4"></i>
                      </div>
                      <div>
                        <h6 class="fw-bold text-light mb-0">{{ activeTrek.assigned_staff.name }}</h6>
                        <span class="text-secondary small">{{ activeTrek.assigned_staff.email }}</span>
                      </div>
                    </div>

                    <div class="small text-secondary mb-3">
                      <div class="mb-2">
                        <strong>Contact:</strong> 
                        <span class="text-light ms-1">{{ activeTrek.assigned_staff.contact || 'N/A' }}</span>
                      </div>
                      <div class="mb-2">
                        <strong>Experience:</strong> 
                        <span class="text-light ms-1">{{ activeTrek.assigned_staff.experience_years }} Years</span>
                      </div>
                      <div class="mb-2">
                        <strong>Specialty:</strong> 
                        <span class="text-light ms-1">{{ activeTrek.assigned_staff.skills || 'General Trekking' }}</span>
                      </div>
                    </div>

                    <div v-if="activeTrek.assigned_staff.bio" class="border-top border-secondary border-opacity-15 pt-3">
                      <span class="text-secondary tiny-text d-block mb-1">About the Guide</span>
                      <p class="text-secondary small mb-0 pre-wrap italic" style="font-style: italic;">
                        "{{ activeTrek.assigned_staff.bio }}"
                      </p>
                    </div>
                  </div>
                  <div v-else class="text-center py-4">
                    <i class="bi bi-person-x text-secondary fs-2 mb-2 d-block"></i>
                    <p class="text-secondary mb-0 small">No guide has been assigned to this trek yet.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer border-top border-secondary border-opacity-15 p-3">
            <button type="button" @click="closeDetails" class="btn btn-outline-secondary border-secondary text-light px-4 rounded-3">Close</button>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import { userService, publicService } from '../../services/api';
import { alertService } from '@/services/alert';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'UserHistory',
  components: {
    DashboardLayout
  },
  data() {
    return {
      history: [],
      loading: true,
      exporting: false,
      activeTrek: null,
      loadingDetailsId: null,
      mobileDetail: null
    };
  },
  methods: {
    async fetchHistory() {
      this.loading = true;
      try {
        const data = await userService.getDashboardSummary();
        this.history = data.booking_history;
      } catch (err) {
        alertService.error('Failed to load trek history.');
      } finally {
        this.loading = false;
      }
    },
    async triggerCSVExport() {
      this.exporting = true;
      try {
        const response = await userService.triggerCSVExport();
        const taskId = response.task_id;
        alertService.success('CSV Export started. Processing in background...');
        this.pollExportStatus(taskId);
      } catch (err) {
        alertService.error('Failed to trigger CSV export.');
        this.exporting = false;
      }
    },
    async pollExportStatus(taskId) {
      try {
        const response = await userService.getExportStatus(taskId);
        if (response.status === 'SUCCESS') {
          const filename = response.result.filename;
          alertService.success('CSV Export ready! Starting download...');
          this.exporting = false;
          
          const token = localStorage.getItem('token');
          const downloadUrl = `/api/user/download-export/${filename}`;
          
          const res = await fetch(downloadUrl, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          const blob = await res.blob();
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', filename);
          document.body.appendChild(link);
          link.click();
          link.parentNode.removeChild(link);
        } else if (response.status === 'FAILURE') {
          alertService.error('Export failed: ' + response.error);
          this.exporting = false;
        } else {
          setTimeout(() => {
            this.pollExportStatus(taskId);
          }, 1500);
        }
      } catch (err) {
        alertService.error('Error checking export status.');
        this.exporting = false;
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
        case 'Completed': return 'bg-info bg-opacity-25 text-info border border-info border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    },
    getOutcomeLabel(b) {
      if (b.status === 'Cancelled') return 'Cancelled';
      if (b.status === 'Booked') {
        const today = new Date();
        const start = b.start_date ? new Date(b.start_date) : null;
        if (start && start < today) {
          return 'Completed';
        }
        return 'Booked';
      }
      return b.status;
    },
    async openTrekDetails(trekId) {
      this.loadingDetailsId = trekId;
      try {
        const data = await publicService.getTrekDetail(trekId);
        this.activeTrek = data;
      } catch (err) {
        alertService.error('Failed to load trek details.');
      } finally {
        this.loadingDetailsId = null;
      }
    },
    closeDetails() {
      this.activeTrek = null;
    }
  },
  mounted() {
    this.fetchHistory();
  }
}
</script>

<style scoped>
.uppercase-label {
  font-size: 0.75rem;
  letter-spacing: 1px;
  text-transform: uppercase;
}
.pre-wrap {
  white-space: pre-wrap;
}
.tiny-text {
  font-size: 0.75rem;
}
.cursor-pointer {
  cursor: pointer;
}
.hover-text-info:hover {
  color: #0dcaf0 !important;
  text-decoration: underline;
}


.detail-backdrop {
  position: fixed; inset: 0; z-index: 1060;
  background: rgba(0,0,0,.65);
  display: flex; align-items: flex-end; justify-content: center;
}
.detail-sheet {
  width: 100%; max-width: 540px;
  background: #0d1117;
  border: 1px solid rgba(100,116,139,.2);
  border-radius: 20px 20px 0 0;
  padding: 16px 20px 36px;
  animation: slideUp .25s cubic-bezier(.4,0,.2,1);
  max-height: 90vh;
  overflow-y: auto;
}
.sheet-handle {
  width: 40px; height: 4px;
  background: rgba(100,116,139,.4);
  border-radius: 2px; margin: 0 auto;
}
@keyframes slideUp {
  from { transform: translateY(100%); }
  to   { transform: translateY(0); }
}
.btn-icon-close {
  background: none; border: none;
  padding: 6px; border-radius: 8px; cursor: pointer;
}
</style>
