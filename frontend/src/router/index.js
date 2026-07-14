import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Treks from '../views/Treks.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import AdminDashboard from '../views/admin/Dashboard.vue';
import AdminTreks from '../views/admin/Treks.vue';
import AdminStaff from '../views/admin/Staff.vue';
import AdminUsers from '../views/admin/Users.vue';
import AdminBookings from '../views/admin/Bookings.vue';
import AdminReports from '../views/admin/Reports.vue';
import StaffDashboard from '../views/staff/Dashboard.vue';
import UserDashboard from '../views/user/Dashboard.vue';
import { authService } from '../services/api';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/treks',
    name: 'Treks',
    component: Treks
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { guestOnly: true }
  },
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, role: 'trekker' }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/treks',
    name: 'AdminTreks',
    component: AdminTreks,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/staff',
    name: 'AdminStaff',
    component: AdminStaff,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: AdminUsers,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/bookings',
    name: 'AdminBookings',
    component: AdminBookings,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/reports',
    name: 'AdminReports',
    component: AdminReports,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/staff/dashboard',
    name: 'StaffDashboard',
    component: StaffDashboard,
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

  // If page is for guests only (e.g. login/register) but user is authenticated, redirect to appropriate dashboard
  if (to.meta.guestOnly && isAuthenticated && currentUser) {
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
