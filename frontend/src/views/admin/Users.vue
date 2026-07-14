<template>
  <DashboardLayout role="admin">
    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-12 text-center text-md-start">
        <h1 class="display-6 fw-bold text-light">Manage <span class="text-gradient">Trekkers</span></h1>
        <p class="text-secondary mb-0">View registered participants and manage account lock/blacklist status</p>
      </div>
    </div>

    <!-- Search bar -->
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

    <!-- Table card -->
    <div class="card bg-dark bg-opacity-50 border-secondary border-opacity-25 shadow rounded-4 p-4">

      <!-- Loading -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-info" role="status"></div>
      </div>

      <!-- Empty -->
      <div v-else-if="users.length === 0" class="text-center py-5">
        <span class="display-4 text-secondary mb-3 d-block"><i class="bi bi-people-fill"></i></span>
        <p class="text-secondary mb-0">No trekkers found in the database.</p>
      </div>

      <template v-else>
        <!-- ── DESKTOP TABLE (md+) ── -->
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

        <!-- ── MOBILE TABLE (< md): 3 cols + View button ── -->
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

        <!-- ── PAGINATION ── -->
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
              <li v-for="p in totalPages" :key="p" class="page-item" :class="{ active: p === currentPage }">
                <button class="page-link bg-dark border-secondary text-white rounded-3"
                  :class="{ 'bg-info border-info text-dark': p === currentPage }"
                  @click="currentPage = p">{{ p }}</button>
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

    <!-- ── MOBILE DETAIL MODAL ── -->
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
    }
  },
  mounted() { this.fetchUsers(); }
}
</script>

<style scoped>
.initial-avatar { width: 32px; height: 32px; font-size: .85rem; background: rgba(0,242,254,.15); }
.badge-active { background: rgba(34,197,94,.2); color: #4ade80; border: 1px solid rgba(34,197,94,.3); }
.badge-locked { background: rgba(239,68,68,.2); color: #f87171; border: 1px solid rgba(239,68,68,.3); }
.avatar-lg { width: 52px; height: 52px; font-size: 1.4rem; background: linear-gradient(135deg,#00f2fe,#4facfe); flex-shrink: 0; }

/* Detail bottom-sheet */
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
</style>
