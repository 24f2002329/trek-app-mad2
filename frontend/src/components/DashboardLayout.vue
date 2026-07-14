<template>
  <div class="dashboard-wrapper d-flex flex-column flex-md-row">
    <!-- ============ DESKTOP SIDEBAR (md+) ============ -->
    <aside class="sidebar d-none d-md-flex flex-column py-4">
      <div class="sidebar-header px-4 mb-4">
        <!-- Brand -->
        <router-link to="/" class="d-flex align-items-center gap-2 text-decoration-none mb-4 pb-3 border-bottom border-secondary border-opacity-20">
          <img src="../assets/images/logo.png" alt="Logo" style="height: 28px; width: auto;" />
          <span class="fw-bold fs-5 text-gradient">TrekSphere</span>
        </router-link>
        <!-- Role Badge -->
        <div class="d-flex align-items-center gap-2">
          <i class="bi fs-5 text-gradient" :class="roleIcon"></i>
          <div>
            <span class="fw-bold text-light d-block">{{ roleLabel }}</span>
            <span class="tiny-text text-secondary">Control Center</span>
          </div>
        </div>
      </div>

      <!-- User Profile Card -->
      <div class="px-3 mb-4">
        <div class="user-card p-3 rounded-3 bg-black bg-opacity-25 border border-secondary border-opacity-10 d-flex align-items-center gap-3">
          <div class="avatar bg-gradient text-white fw-bold rounded-circle d-flex align-items-center justify-content-center">
            {{ userInitial }}
          </div>
          <div class="overflow-hidden">
            <h6 class="text-light mb-0 text-truncate">{{ user?.name || 'User' }}</h6>
            <small class="text-secondary text-truncate d-block">{{ user?.email }}</small>
          </div>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-grow-1 px-3 d-flex flex-column gap-2">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-btn py-2 px-3 rounded-3 d-flex align-items-center gap-3 text-secondary text-decoration-none"
          :class="{ active: isActive(item.path) }"
        >
          <i class="bi fs-5" :class="item.icon"></i>
          <span class="fw-medium">{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- Sidebar Footer (Logout) -->
      <div class="px-3 mt-auto pt-3 border-top border-secondary border-opacity-10">
        <button @click="logout" class="btn btn-outline-danger w-100 py-2 d-flex align-items-center justify-content-center gap-2 rounded-3 border-opacity-20">
          <i class="bi bi-box-arrow-right"></i>
          <span>Logout</span>
        </button>
      </div>
    </aside>

    <!-- ============ MOBILE HEADERNavbar (< md) ============ -->
    <header class="mobile-topbar d-flex d-md-none align-items-center justify-content-between px-3">
      <!-- Brand -->
      <router-link to="/" class="d-flex align-items-center gap-2 text-decoration-none">
        <img src="../assets/images/logo.png" alt="Logo" style="height: 24px; width: auto;" />
        <span class="fw-bold text-gradient">TrekSphere</span>
      </router-link>

      <!-- Right: user initial + hamburger -->
      <div class="d-flex align-items-center gap-2">
        <div class="avatar-sm bg-gradient text-white fw-bold rounded-circle d-flex align-items-center justify-content-center">
          {{ userInitial }}
        </div>
        <button class="hamburger-btn" @click="drawerOpen = true" aria-label="Open menu">
          <i class="bi bi-list fs-4 text-light"></i>
        </button>
      </div>
    </header>

    <!-- ============ SLIDE-IN DRAWER (mobile) ============ -->
    <Teleport to="body">
      <!-- Backdrop -->
      <transition name="fade-backdrop">
        <div v-if="drawerOpen" class="drawer-backdrop" @click="drawerOpen = false"></div>
      </transition>

      <!-- Drawer Panel -->
      <transition name="slide-drawer">
        <div v-if="drawerOpen" class="drawer-panel d-flex flex-column py-4 px-3">
          <!-- Drawer Header -->
          <div class="d-flex align-items-center justify-content-between mb-4 pb-3 border-bottom border-secondary border-opacity-20">
            <div class="d-flex align-items-center gap-2">
              <i class="bi fs-5 text-gradient" :class="roleIcon"></i>
              <div>
                <span class="fw-bold text-light d-block lh-1">{{ roleLabel }}</span>
                <span class="tiny-text text-secondary">{{ user?.name }}</span>
              </div>
            </div>
            <button class="btn-icon-close" @click="drawerOpen = false">
              <i class="bi bi-x-lg text-secondary"></i>
            </button>
          </div>

          <!-- Nav Links -->
          <nav class="d-flex flex-column gap-1 flex-grow-1">
            <router-link
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              class="drawer-nav-btn py-3 px-3 rounded-3 d-flex align-items-center gap-3 text-secondary text-decoration-none"
              :class="{ active: isActive(item.path) }"
              @click="drawerOpen = false"
            >
              <i class="bi fs-5" :class="item.icon"></i>
              <span class="fw-medium fs-6">{{ item.label }}</span>
            </router-link>
          </nav>

          <!-- Drawer Logout -->
          <div class="mt-auto pt-3 border-top border-secondary border-opacity-10">
            <button @click="logout" class="btn btn-outline-danger w-100 py-2 d-flex align-items-center justify-content-center gap-2 rounded-3">
              <i class="bi bi-box-arrow-right"></i>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- ============ MAIN CONTENT AREA ============ -->
    <div class="dashboard-content flex-grow-1">
      <div class="content-inner p-3 p-md-5">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '../services/api';

export default {
  name: 'DashboardLayout',
  props: {
    role: {
      type: String,
      required: true,
      validator: value => ['admin', 'staff', 'user'].includes(value)
    }
  },
  data() {
    return {
      user: null,
      drawerOpen: false
    };
  },
  computed: {
    roleLabel() {
      if (this.role === 'admin') return 'Admin';
      if (this.role === 'staff') return 'Staff';
      return 'Trekker';
    },
    roleIcon() {
      if (this.role === 'admin') return 'bi-shield-lock-fill';
      if (this.role === 'staff') return 'bi-compass';
      return 'bi-person-circle';
    },
    userInitial() {
      return this.user?.name ? this.user.name.charAt(0).toUpperCase() : 'U';
    },
    navItems() {
      if (this.role === 'admin') {
        return [
          { path: '/admin/dashboard', label: 'Overview',  icon: 'bi-grid-1x2-fill' },
          { path: '/admin/treks',     label: 'Treks',    icon: 'bi-compass' },
          { path: '/admin/staff',     label: 'Staff Guide', icon: 'bi-person-badge' },
          { path: '/admin/users',     label: 'Trekkers',  icon: 'bi-people' },
          { path: '/admin/bookings',  label: 'Bookings',  icon: 'bi-calendar-check' },
          { path: '/admin/reports',   label: 'Analytics', icon: 'bi-bar-chart-line' }
        ];
      }
      if (this.role === 'staff') {
        return [
          { path: '/staff/dashboard', label: 'Dashboard', icon: 'bi-grid-1x2-fill' },
          { path: '/staff/treks', label: 'My Treks', icon: 'bi-compass' },
          { path: '/staff/participants', label: 'Participants', icon: 'bi-people' },
          { path: '/staff/profile', label: 'Profile', icon: 'bi-person-circle' }
        ];
      }
      return [
        { path: '/dashboard', label: 'Dashboard',  icon: 'bi-grid-1x2-fill' },
        { path: '/browse-treks', label: 'Browse Treks', icon: 'bi-compass' },
        { path: '/my-bookings', label: 'My Bookings', icon: 'bi-calendar-check' },
        { path: '/history', label: 'History', icon: 'bi-clock-history' },
        { path: '/profile', label: 'Profile', icon: 'bi-person-circle' }
      ];
    }
  },
  watch: {
    // Close drawer on route change
    '$route'() {
      this.drawerOpen = false;
    },
    // Lock body scroll when drawer is open
    drawerOpen(val) {
      document.body.style.overflow = val ? 'hidden' : '';
    }
  },
  methods: {
    isActive(path) {
      return this.$route.path === path;
    },
    logout() {
      authService.logout();
      this.$router.push('/login');
    }
  },
  mounted() {
    this.user = authService.getCurrentUser();
  },
  beforeUnmount() {
    document.body.style.overflow = '';
  }
}
</script>

<style scoped>
/* ===== WRAPPER ===== */
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
}

/* ===== DESKTOP SIDEBAR ===== */
.sidebar {
  width: 260px;
  min-width: 260px;
  background: rgba(8, 12, 20, 0.98);
  border-right: 1px solid rgba(100, 116, 139, 0.15);
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 10;
  overflow-y: auto;
}

.avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #00f2fe, #4facfe);
  font-size: 1.2rem;
  flex-shrink: 0;
}

.avatar-sm {
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #00f2fe, #4facfe);
  font-size: 0.9rem;
  flex-shrink: 0;
}

.nav-btn {
  transition: all 0.22s ease;
  border: 1px solid transparent;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff !important;
}

.nav-btn.active {
  background: rgba(0, 242, 254, 0.1);
  color: #00f2fe !important;
  border-color: rgba(0, 242, 254, 0.15);
}

/* ===== DESKTOP CONTENT ===== */
.dashboard-content {
  overflow-x: hidden;
  min-height: 100vh;
  background: radial-gradient(circle at 10% 20%, rgba(10, 14, 23, 0.95) 0%, rgba(15, 23, 42, 0.9) 90%);
}

/* ===== MOBILE TOP BAR ===== */
.mobile-topbar {
  height: 56px;
  background: rgba(8, 12, 20, 0.98);
  border-bottom: 1px solid rgba(100, 116, 139, 0.15);
  position: sticky;
  top: 0;
  z-index: 50;
  flex-shrink: 0;
}

.hamburger-btn {
  background: none;
  border: none;
  padding: 4px 6px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  line-height: 1;
}

.hamburger-btn:hover {
  background: rgba(255, 255, 255, 0.06);
}

/* ===== SLIDE-IN DRAWER ===== */
.drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  z-index: 1040;
}

.drawer-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 280px;
  height: 100dvh;
  background: rgba(8, 12, 20, 0.99);
  border-left: 1px solid rgba(100, 116, 139, 0.18);
  z-index: 1050;
  overflow-y: auto;
}

.drawer-nav-btn {
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.drawer-nav-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff !important;
}

.drawer-nav-btn.active {
  background: rgba(0, 242, 254, 0.1);
  color: #00f2fe !important;
  border-color: rgba(0, 242, 254, 0.15);
}

.btn-icon-close {
  background: none;
  border: none;
  padding: 6px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  line-height: 1;
}

.btn-icon-close:hover {
  background: rgba(255,255,255,0.06);
}

/* ===== DRAWER TRANSITIONS ===== */
.fade-backdrop-enter-active,
.fade-backdrop-leave-active {
  transition: opacity 0.25s ease;
}
.fade-backdrop-enter-from,
.fade-backdrop-leave-to {
  opacity: 0;
}

.slide-drawer-enter-active,
.slide-drawer-leave-active {
  transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-drawer-enter-from,
.slide-drawer-leave-to {
  transform: translateX(100%);
}

/* ===== MISC ===== */
.tiny-text {
  font-size: 0.65rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>
