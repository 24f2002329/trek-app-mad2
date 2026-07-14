import { createRouter, createWebHistory } from 'vue-router';
import { authService } from '../services/api';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/treks',
    name: 'Treks',
    component: () => import('../views/Treks.vue')
  },
  {
    path: '/public-dashboard',
    name: 'PublicDashboard',
    component: () => import('../views/PublicDashboard.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: () => import('../views/user/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'trekker' }
  },
  {
    path: '/browse-treks',
    name: 'UserBrowseTreks',
    component: () => import('../views/user/BrowseTreks.vue'),
    meta: { requiresAuth: true, role: 'trekker' }
  },
  {
    path: '/my-bookings',
    name: 'UserBookings',
    component: () => import('../views/user/Bookings.vue'),
    meta: { requiresAuth: true, role: 'trekker' }
  },
  {
    path: '/history',
    name: 'UserHistory',
    component: () => import('../views/user/History.vue'),
    meta: { requiresAuth: true, role: 'trekker' }
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: () => import('../views/user/Profile.vue'),
    meta: { requiresAuth: true, role: 'trekker' }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/treks',
    name: 'AdminTreks',
    component: () => import('../views/admin/Treks.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/staff',
    name: 'AdminStaff',
    component: () => import('../views/admin/Staff.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/admin/Users.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/bookings',
    name: 'AdminBookings',
    component: () => import('../views/admin/Bookings.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/reports',
    name: 'AdminReports',
    component: () => import('../views/admin/Reports.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/staff/dashboard',
    name: 'StaffDashboard',
    component: () => import('../views/staff/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'trek_staff' }
  },
  {
    path: '/staff/treks',
    name: 'StaffTreks',
    component: () => import('../views/staff/MyTreks.vue'),
    meta: { requiresAuth: true, role: 'trek_staff' }
  },
  {
    path: '/staff/participants',
    name: 'StaffParticipants',
    component: () => import('../views/staff/Participants.vue'),
    meta: { requiresAuth: true, role: 'trek_staff' }
  },
  {
    path: '/staff/profile',
    name: 'StaffProfile',
    component: () => import('../views/staff/Profile.vue'),
    meta: { requiresAuth: true, role: 'trek_staff' }
  },

  // Fallback redirect
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated();
  const currentUser = authService.getCurrentUser();

  // If user is authenticated and attempts to access the home page '/' or guest-only pages (e.g. login/register), redirect to appropriate dashboard
  if ((to.path === '/' || to.meta.guestOnly) && isAuthenticated && currentUser) {
    if (currentUser.role === 'admin') {
      return next('/admin/dashboard');
    } else if (currentUser.role === 'trek_staff') {
      return next('/staff/dashboard');
    } else {
      return next('/dashboard');
    }
  }

  // If page requires auth
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      return next({ path: '/login', query: { redirect: to.fullPath } });
    }

    // Role verification
    if (to.meta.role && currentUser && currentUser.role !== to.meta.role) {
      // Role mismatch, send user to their own dashboard
      if (currentUser.role === 'admin') {
        return next('/admin/dashboard');
      } else if (currentUser.role === 'trek_staff') {
        return next('/staff/dashboard');
      } else {
        return next('/dashboard');
      }
    }
  }

  next();
});

export default router;
