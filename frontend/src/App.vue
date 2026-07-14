<template>
  <div id="app" class="d-flex flex-column min-vh-100 bg-dark text-light position-relative">
    <AlertContainer />
    <ConfirmContainer />
    <!-- Show Navbar only on non-dashboard routes -->
    <Navbar v-if="!isDashboardRoute" />
    
    <main class="flex-grow-1 position-relative z-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Show footer only on non-dashboard routes -->
    <footer v-if="!isDashboardRoute" class="py-4 text-center border-top border-secondary border-opacity-20 text-secondary z-1 mt-auto">
      <div class="container">
        <small>&copy; 2026 Trekking Management Application V2. All rights reserved  <br> Made with ❤️ by Devendra.</small>
      </div>
    </footer>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';
import AlertContainer from './components/AlertContainer.vue';
import ConfirmContainer from './components/ConfirmContainer.vue';

export default {
  name: 'App',
  components: {
    Navbar,
    AlertContainer,
    ConfirmContainer
  },
  computed: {
    isDashboardRoute() {
      const path = this.$route?.path || '';
      return path.startsWith('/admin') || path.startsWith('/staff') || path === '/dashboard';
    }
  }
}
</script>

<style>
/* Custom transitions for route swapping */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(4px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
