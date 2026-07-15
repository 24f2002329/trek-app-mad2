<template>
  <DashboardLayout role="admin">
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Manage <span class="text-gradient">Trekkers</span></h1>
        <p class="text-secondary mb-0">View registered participants and manage account lock/blacklist status</p>
      </div>
    </div>


    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 rounded-4 p-4 mb-4 shadow">
      <div class="input-group">
        <span class="input-group-text bg-black bg-opacity-25 border-secondary text-secondary"><i class="bi bi-search"></i></span>
        <input
          v-model="filters.search"
          @input="onSearch"
          type="text"
          class="form-control bg-black bg-opacity-25 border-secondary text-light"
          placeholder="Search trekkers by name, email, or ID..."
        />
      </div>
    </div>


    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4">

 
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-info" role="status"></div>
      </div>


      <div v-else-if="users.length === 0" class="text-center py-5">
        <span class="display-4 text-secondary mb-3 d-block"><i class="bi bi-people-fill"></i></span>
        <p class="text-secondary mb-0">No trekkers found in the database.</p>
      </div>

      <template v-else>
        <!-- DESKTOP TABLE -->
        <div class="d-none d-md-block table-responsive">
          <table class="table table-dark table-hover border-secondary border-opacity-10 align-middle">
            <thead>
              <tr>
                <th class="text-secondary border-secondary">ID</th>
                <th class="text-secondary border-secondary">Name</th>
                <th class="text-secondary border-secondary">Email</th>
                <th class="text-secondary border-secondary text-center">Bookings</th>
                <th class="text-secondary border-secondary">Joined</th>
                <th class="text-secondary border-secondary text-center">Status</th>
                <th class="text-secondary border-secondary text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in paginated" :key="user.id">
                <td class="border-secondary border-opacity-10 text-info fw-bold">#{{ user.id }}</td>
                <td class="border-secondary border-opacity-10">
                  <div class="d-flex align-items-center gap-2">
                    <div class="initial-avatar text-info fw-bold rounded-circle d-flex align-items-center justify-content-center">
                      {{ user.name.charAt(0).toUpperCase() }}
                    </div>
                    <span class="fw-bold text-light">{{ user.name }}</span>
                  </div>
                </td>
                <td class="border-secondary border-opacity-10 text-secondary">{{ user.email }}</td>
                <td class="border-secondary border-opacity-10 text-center">
                  <span class="badge bg-secondary rounded-pill px-2 py-1">{{ user.bookings_count }}</span>
                </td>
                <td class="border-secondary border-opacity-10 text-secondary small">{{ formatDate(user.created_at) }}</td>
                <td class="border-secondary border-opacity-10 text-center">
                  <span class="badge px-3 py-1 rounded-pill" :class="user.is_active ? 'badge-active' : 'badge-locked'">
                    {{ user.is_active ? 'Active' : 'Locked' }}
                  </span>
                </td>
                <td class="border-secondary border-opacity-10 text-end">
                  <button @click="openDetail(user)" class="btn btn-sm btn-outline-info rounded-3 py-1 px-3 me-2">
                    <i class="bi bi-eye-fill"></i> View
                  </button>
                  <button @click="toggleUserStatus(user)" class="btn btn-sm rounded-3 py-1 px-3"
                    :class="user.is_active ? 'btn-outline-danger' : 'btn-outline-success'">
                    <i class="bi" :class="user.is_active ? 'bi-lock-fill' : 'bi-unlock-fill'"></i>
                    {{ user.is_active ? 'Block' : 'Unlock' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- MOBILE TABLE -->
        <div class="d-md-none table-responsive">
          <table class="table table-dark table-sm border-secondary border-opacity-10 align-middle">
            <thead>
              <tr>
                <th class="text-secondary border-secondary">Name</th>
                <th class="text-secondary border-secondary text-center">Status</th>
                <th class="text-secondary border-secondary text-end">Details</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in paginated" :key="user.id">
                <td class="border-secondary border-opacity-10">
                  <div class="d-flex align-items-center gap-2">
                    <div class="initial-avatar text-info fw-bold rounded-circle d-flex align-items-center justify-content-center" style="width:28px;height:28px;font-size:.75rem;">
                      {{ user.name.charAt(0).toUpperCase() }}
                    </div>
                    <span class="text-light small fw-bold text-truncate" style="max-width:110px;">{{ user.name }}</span>
                  </div>
                </td>
                <td class="border-secondary border-opacity-10 text-center">
                  <span class="badge rounded-pill" :class="user.is_active ? 'badge-active' : 'badge-locked'">
                    {{ user.is_active ? 'Active' : 'Locked' }}
                  </span>
                </td>
                <td class="border-secondary border-opacity-10 text-end">
                  <button @click="openDetail(user)" class="btn btn-outline-info btn-sm rounded-3 px-2 py-1">
                    <i class="bi bi-eye-fill"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mt-3 pt-3 border-top border-secondary border-opacity-10">
          <small class="text-secondary">
            Showing {{ (currentPage - 1) * perPage + 1 }}–{{ Math.min(currentPage * perPage, filteredUsers.length) }}
            of {{ filteredUsers.length }} trekkers
          </small>
          <nav>
            <ul class="pagination pagination-sm mb-0 gap-1">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link bg-dark border-secondary text-white rounded-3" @click="currentPage--">
                  <i class="bi bi-chevron-left"></i>
                </button>
              </li>
              <li v-for="(p, idx) in visiblePages" :key="idx" class="page-item" :class="{ active: p === currentPage, disabled: p === '...' }">
                <button class="page-link bg-dark border-secondary text-white rounded-3"
                  :class="{ 'bg-info border-info text-dark': p === currentPage }"
                  :disabled="p === '...'"
                  @click="p !== '...' && (currentPage = p)">{{ p }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link bg-dark border-secondary text-white rounded-3" @click="currentPage++">
                  <i class="bi bi-chevron-right"></i>
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </template>
    </div>

    <Teleport to="body">
      <div v-if="detailUser" class="detail-backdrop" @click.self="detailUser = null">
        <div class="detail-sheet">
          <!-- Handle bar -->
          <div class="text-center mb-3"><div class="sheet-handle"></div></div>

          <div class="d-flex justify-content-between align-items-start mb-4">
            <div class="d-flex align-items-center gap-3">
              <div class="avatar-lg bg-gradient text-white fw-bold rounded-circle d-flex align-items-center justify-content-center">
                {{ detailUser.name.charAt(0).toUpperCase() }}
              </div>
              <div>
                <h5 class="text-light fw-bold mb-0">{{ detailUser.name }}</h5>
                <small class="text-secondary">#{{ detailUser.id }}</small>
              </div>
            </div>
            <button class="btn-icon-close" @click="detailUser = null"><i class="bi bi-x-lg text-secondary"></i></button>
          </div>

          <div class="list-group list-group-flush mb-4">
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
              <span class="text-secondary small">Email</span>
              <span class="text-light small text-end" style="max-width:60%;word-break:break-all;">{{ detailUser.email }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
              <span class="text-secondary small">Bookings</span>
              <span class="badge bg-secondary rounded-pill">{{ detailUser.bookings_count }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
              <span class="text-secondary small">Joined</span>
              <span class="text-light small">{{ formatDate(detailUser.created_at) }}</span>
            </div>
            <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
              <span class="text-secondary small">Status</span>
              <span class="badge rounded-pill" :class="detailUser.is_active ? 'badge-active' : 'badge-locked'">
                {{ detailUser.is_active ? 'Active' : 'Locked' }}
              </span>
            </div>
          </div>

          <button @click="toggleUserStatus(detailUser); detailUser = null"
            class="btn w-100 py-2 rounded-3"
            :class="detailUser.is_active ? 'btn-outline-danger' : 'btn-outline-success'">
            <i class="bi me-2" :class="detailUser.is_active ? 'bi-lock-fill' : 'bi-unlock-fill'"></i>
            {{ detailUser.is_active ? 'Block Account' : 'Unlock Account' }}
          </button>
        </div>
      </div>
    </Teleport>


    <Teleport to="body">
      <div v-if="viewUser" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.88); backdrop-filter: blur(6px); z-index: 1060;" @click.self="closeView">
        <div class="modal-dialog modal-dialog-centered modal-xl modal-dialog-scrollable">
          <div class="modal-content bg-dark border-secondary border-opacity-50 text-light rounded-4 shadow-lg">
            
            <div class="modal-header border-bottom border-secondary border-opacity-15 p-4">
              <div class="d-flex align-items-center gap-3">
                <div class="initial-avatar-lg text-info fw-bold rounded-circle d-flex align-items-center justify-content-center">
                  {{ viewUser.name.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <h4 class="fw-bold text-light mb-0">{{ viewUser.name }}</h4>
                  <small class="text-secondary">{{ viewUser.email }} &bull; ID #{{ viewUser.id }}</small>
                </div>
                <span class="badge rounded-pill ms-2" :class="viewUser.is_active ? 'badge-active' : 'badge-locked'">
                  {{ viewUser.is_active ? 'Active' : 'Locked' }}
                </span>
              </div>
              <button type="button" @click="closeView" class="btn-close btn-close-white ms-auto"></button>
            </div>


            <div class="modal-body p-4">
              <div v-if="viewLoading" class="text-center py-5">
                <div class="spinner-border text-info" role="status"></div>
              </div>
              <div v-else class="row g-4">


                <div class="col-lg-6">
                  <div class="p-3 rounded-4 bg-black bg-opacity-25 border border-secondary border-opacity-15">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                      <h6 class="text-gradient fw-bold uppercase-label mb-0">Profile Information</h6>
                      <button v-if="!editMode" @click="startEdit" class="btn btn-sm btn-outline-info rounded-3 px-3">
                        <i class="bi bi-pencil me-1"></i>Edit
                      </button>
                    </div>

                    <div v-if="!editMode" class="list-group list-group-flush">
                      <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
                        <span class="text-secondary small">Full Name</span>
                        <span class="text-light small fw-semibold">{{ viewUser.name }}</span>
                      </div>
                      <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
                        <span class="text-secondary small">Phone</span>
                        <span class="text-light small">{{ viewUser.phone || '—' }}</span>
                      </div>
                      <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
                        <span class="text-secondary small">Blood Group</span>
                        <span class="text-light small">{{ viewUser.blood_group || '—' }}</span>
                      </div>
                      <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
                        <span class="text-secondary small">Medical Conditions</span>
                        <span class="text-light small text-end" style="max-width:55%;">{{ viewUser.medical_conditions || '—' }}</span>
                      </div>
                      <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
                        <span class="text-secondary small">Joined</span>
                        <span class="text-light small">{{ formatDate(viewUser.created_at) }}</span>
                      </div>
                    </div>


                    <div v-else>
                      <div class="mb-3">
                        <label class="form-label text-secondary small">Full Name</label>
                        <input v-model="editForm.name" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light" />
                      </div>
                      <div class="mb-3">
                        <label class="form-label text-secondary small">Phone</label>
                        <input v-model="editForm.phone" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light" placeholder="+91 ..." />
                      </div>
                      <div class="mb-3">
                        <label class="form-label text-secondary small">Blood Group</label>
                        <select v-model="editForm.blood_group" class="form-select bg-black bg-opacity-25 border-secondary text-light">
                          <option value="">Not specified</option>
                          <option v-for="bg in ['A+','A-','B+','B-','O+','O-','AB+','AB-']" :key="bg" :value="bg">{{ bg }}</option>
                        </select>
                      </div>
                      <div class="mb-3">
                        <label class="form-label text-secondary small">Medical Conditions</label>
                        <textarea v-model="editForm.medical_conditions" class="form-control bg-black bg-opacity-25 border-secondary text-light" rows="2" placeholder="None"></textarea>
                      </div>
                      <div class="d-flex gap-2 mt-3">
                        <button @click="saveEdit" :disabled="saving" class="btn btn-glow px-4 rounded-3">
                          <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
                          Save Changes
                        </button>
                        <button @click="editMode = false" class="btn btn-outline-secondary border-secondary text-light rounded-3">Cancel</button>
                      </div>
                    </div>
                  </div>


                  <div class="p-3 rounded-4 bg-black bg-opacity-25 border border-secondary border-opacity-15 mt-3">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                      <h6 class="text-gradient fw-bold uppercase-label mb-0">Emergency Contact</h6>
                      <button v-if="!editMode" @click="startEdit" class="btn btn-sm btn-outline-info rounded-3 px-3">
                        <i class="bi bi-pencil me-1"></i>Edit
                      </button>
                    </div>
                    <div v-if="!editMode" class="list-group list-group-flush">
                      <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
                        <span class="text-secondary small">Contact Name</span>
                        <span class="text-light small">{{ viewUser.emergency_contact_name || '—' }}</span>
                      </div>
                      <div class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 d-flex justify-content-between">
                        <span class="text-secondary small">Contact Phone</span>
                        <span class="text-light small">{{ viewUser.emergency_contact_phone || '—' }}</span>
                      </div>
                    </div>
                    <div v-else>
                      <div class="mb-3">
                        <label class="form-label text-secondary small">Emergency Contact Name</label>
                        <input v-model="editForm.emergency_contact_name" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light" />
                      </div>
                      <div class="mb-0">
                        <label class="form-label text-secondary small">Emergency Contact Phone</label>
                        <input v-model="editForm.emergency_contact_phone" type="text" class="form-control bg-black bg-opacity-25 border-secondary text-light" />
                      </div>
                    </div>
                  </div>


                  <div class="p-3 rounded-4 bg-black bg-opacity-25 border border-secondary border-opacity-15 mt-3">
                    <h6 class="text-gradient fw-bold uppercase-label mb-3">Account Actions</h6>
                    <button @click="toggleUserStatus(viewUser); closeView()" class="btn w-100 py-2 rounded-3"
                      :class="viewUser.is_active ? 'btn-outline-danger' : 'btn-outline-success'">
                      <i class="bi me-2" :class="viewUser.is_active ? 'bi-lock-fill' : 'bi-unlock-fill'"></i>
                      {{ viewUser.is_active ? 'Block Account' : 'Unlock Account' }}
                    </button>
                  </div>
                </div>


                <div class="col-lg-6">
                  <div class="p-3 rounded-4 bg-black bg-opacity-25 border border-secondary border-opacity-15 h-100">
                    <h6 class="text-gradient fw-bold uppercase-label mb-3">Booking History <span class="badge bg-secondary rounded-pill ms-2">{{ viewUser.bookings_count }}</span></h6>
                    <div v-if="viewUser.bookings && viewUser.bookings.length === 0" class="text-center py-4">
                      <i class="bi bi-calendar-x text-secondary fs-2 d-block mb-2"></i>
                      <p class="text-secondary small mb-0">No bookings yet.</p>
                    </div>
                    <div v-else class="list-group list-group-flush" style="max-height: 460px; overflow-y: auto;">
                      <div v-for="b in viewUser.bookings" :key="b.booking_id" class="list-group-item bg-transparent border-secondary border-opacity-15 px-0 py-3">
                        <div class="d-flex justify-content-between align-items-start">
                          <div>
                            <p class="text-light fw-semibold mb-1 small">{{ b.trek_name }}</p>
                            <p class="text-secondary mb-1" style="font-size:.75rem;">
                              <i class="bi bi-geo-alt me-1 text-danger"></i>{{ b.location }}
                              &bull; <i class="bi bi-calendar-event me-1 text-warning"></i>{{ formatDate(b.start_date) }}
                            </p>
                            <p class="text-secondary mb-0" style="font-size:.75rem;">
                              Slots: {{ b.slots_booked }} &bull; Booked: {{ formatDate(b.booking_date) }}
                            </p>
                          </div>
                          <div class="text-end">
                            <span class="badge rounded-pill d-block mb-1" :class="getStatusClass(b.status)">{{ b.status }}</span>
                            <span class="badge rounded-pill" :class="b.payment_status === 'Paid' ? 'bg-success bg-opacity-25 text-success border border-success border-opacity-25' : 'bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25'">{{ b.payment_status }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </DashboardLayout>
</template>

<script>
import { adminService } from '../../services/api';
import { alertService } from '@/services/alert';
import { confirmService } from '@/services/confirm';
import DashboardLayout from '../../components/DashboardLayout.vue';

export default {
  name: 'AdminUsers',
  components: { DashboardLayout },
  data() {
    return {
      users: [],
      loading: true,
      detailUser: null,
      viewUser: null,
      viewLoading: false,
      editMode: false,
      editForm: {},
      saving: false,
      currentPage: 1,
      perPage: 10,
      filters: { search: '' }
    };
  },
  computed: {
    filteredUsers() {
      if (!this.filters.search) return this.users;
      const q = this.filters.search.toLowerCase();
      return this.users.filter(u =>
        u.name.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q) ||
        String(u.id).includes(q)
      );
    },
    totalPages() {
      return Math.max(1, Math.ceil(this.filteredUsers.length / this.perPage));
    },
    paginated() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filteredUsers.slice(start, start + this.perPage);
    },
    visiblePages() {
      const range = [];
      const total = this.totalPages;
      const current = this.currentPage;
      
      if (total <= 7) {
        for (let i = 1; i <= total; i++) {
          range.push(i);
        }
        return range;
      }
      
      range.push(1);
      
      let start = Math.max(2, current - 1);
      let end = Math.min(total - 1, current + 1);
      
      if (current <= 3) {
        end = 4;
      } else if (current >= total - 2) {
        start = total - 3;
      }
      
      if (start > 2) {
        range.push('...');
      }
      
      for (let i = start; i <= end; i++) {
        range.push(i);
      }
      
      if (end < total - 1) {
        range.push('...');
      }
      
      range.push(total);
      return range;
    }
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      try {
        this.users = await adminService.getUsers({ search: '' });
      } catch (err) {
        console.error('Failed to load users list', err);
      } finally {
        this.loading = false;
      }
    },
    onSearch() {
      this.currentPage = 1;
    },
    openDetail(user) {
      this.detailUser = user;
    },
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        return new Date(dateStr).toLocaleDateString('en-GB', { timeZone: 'Asia/Kolkata' });
      } catch { return dateStr; }
    },
    async toggleUserStatus(user) {
      const msg = user.is_active
        ? `Deactivate / blacklist "${user.name}"? They will be blocked from logging in.`
        : `Unlock and activate account for "${user.name}"?`;
      
      const confirmed = await confirmService.ask(msg, {
        title: user.is_active ? 'Block Account' : 'Unlock Account',
        isDanger: user.is_active
      });
      
      if (confirmed) {
        try {
          await adminService.toggleUserStatus(user.id, !user.is_active);
          await this.fetchUsers();
          alertService.success('Status updated successfully!');
        } catch { alertService.error('Failed to update status.'); }
      }
    },
    async openDetail(user) {
      this.viewUser = null;
      this.editMode = false;
      this.viewLoading = true;
      this.viewUser = { ...user, bookings: [] };
      try {
        const detail = await adminService.getUserDetail(user.id);
        this.viewUser = detail;
      } catch (err) {
        alertService.error('Failed to load trekker details.');
        this.viewUser = null;
      } finally {
        this.viewLoading = false;
      }
    },
    closeView() {
      this.viewUser = null;
      this.editMode = false;
    },
    startEdit() {
      this.editForm = {
        name: this.viewUser.name,
        phone: this.viewUser.phone || '',
        blood_group: this.viewUser.blood_group || '',
        medical_conditions: this.viewUser.medical_conditions || '',
        emergency_contact_name: this.viewUser.emergency_contact_name || '',
        emergency_contact_phone: this.viewUser.emergency_contact_phone || ''
      };
      this.editMode = true;
    },
    async saveEdit() {
      this.saving = true;
      try {
        await adminService.updateUserDetail(this.viewUser.id, this.editForm);
        alertService.success('Trekker details updated successfully!');

        const detail = await adminService.getUserDetail(this.viewUser.id);
        this.viewUser = detail;
        this.editMode = false;
        await this.fetchUsers();
      } catch (err) {
        alertService.error(err.response?.data?.message || 'Failed to update trekker details.');
      } finally {
        this.saving = false;
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 'Booked': return 'bg-success bg-opacity-25 text-success border border-success border-opacity-25';
        case 'Cancelled': return 'bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25';
        case 'Completed': return 'bg-info bg-opacity-25 text-info border border-info border-opacity-25';
        default: return 'bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25';
      }
    }
  },
  mounted() { this.fetchUsers(); }
}
</script>

<style scoped>
.initial-avatar { width: 32px; height: 32px; font-size: .85rem; background: rgba(0,242,254,.15); }
.initial-avatar-lg { width: 56px; height: 56px; font-size: 1.5rem; background: linear-gradient(135deg, rgba(0,242,254,.2), rgba(79,172,254,.2)); flex-shrink: 0; }
.badge-active { background: rgba(34,197,94,.2); color: #4ade80; border: 1px solid rgba(34,197,94,.3); }
.badge-locked { background: rgba(239,68,68,.2); color: #f87171; border: 1px solid rgba(239,68,68,.3); }
.avatar-lg { width: 52px; height: 52px; font-size: 1.4rem; background: linear-gradient(135deg,#00f2fe,#4facfe); flex-shrink: 0; }
.uppercase-label { font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; }


.detail-backdrop {
  position: fixed; inset: 0; z-index: 1060;
  background: rgba(0,0,0,.6);
  display: flex; align-items: flex-end; justify-content: center;
}
.detail-sheet {
  width: 100%; max-width: 540px;
  background: #0d1117;
  border: 1px solid rgba(100,116,139,.2);
  border-radius: 20px 20px 0 0;
  padding: 16px 20px 32px;
  animation: slideUp .25s cubic-bezier(.4,0,.2,1);
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
.page-link { min-width: 32px; text-align: center; }
.modal-content { background: #0d1117; }
.form-control, .form-select { color: #e2e8f0 !important; }
.form-control::placeholder { color: #64748b; }
</style>

