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
        <h5 class="text-light mb-1 h6">TrekSphere</h5>
        <p class="mb-1 text-secondary small">MAD-2 Course Project</p>
        <p class="mb-1 text-secondary small">Developed by <strong>Devendra Chouhan</strong></p>
        <p class="mb-0 text-secondary small">BS in Data Science and Applications | IIT Madras</p>
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
      return this.$route?.meta?.requiresAuth === true;
    }
  }
}
</script>

<style>
.fade-enter-active, .fade-leave-active {
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
