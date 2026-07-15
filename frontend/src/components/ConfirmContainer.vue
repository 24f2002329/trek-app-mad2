<template>
  <Teleport to="body">
    <transition name="fade">
      <div v-if="state.show" class="confirm-backdrop d-flex align-items-center justify-content-center" @click.self="cancel">
        <div class="confirm-card bg-dark border border-secondary border-opacity-25 rounded-4 p-4 shadow-lg text-center" style="max-width: 400px; width: 90%;">

          <div class="confirm-icon-container mx-auto mb-3 d-flex align-items-center justify-content-center rounded-circle" :class="state.isDanger ? 'bg-danger bg-opacity-10 text-danger border border-danger border-opacity-25' : 'bg-warning bg-opacity-10 text-warning border border-warning border-opacity-25'">
            <i class="bi fs-3" :class="state.isDanger ? 'bi-exclamation-octagon-fill' : 'bi-question-circle-fill'"></i>
          </div>
          
          <h5 class="text-light fw-bold mb-2">{{ state.title }}</h5>
          <p class="text-secondary small mb-4 white-space-pre-line">{{ state.message }}</p>
          
          <div class="d-flex gap-3 justify-content-center">
            <button type="button" class="btn btn-outline-secondary px-4 py-2 rounded-3 w-50" @click="cancel">
              {{ state.cancelText }}
            </button>
            <button type="button" class="btn px-4 py-2 rounded-3 w-50" :class="state.isDanger ? 'btn-danger' : 'btn-glow'" @click="confirm">
              {{ state.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script>
import { confirmState } from '../services/confirm';

export default {
  name: 'ConfirmContainer',
  computed: {
    state() {
      return confirmState;
    }
  },
  methods: {
    confirm() {
      if (confirmState.resolve) confirmState.resolve();
    },
    cancel() {
      if (confirmState.reject) confirmState.reject();
    }
  }
}
</script>

<style scoped>
.confirm-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(10, 14, 23, 0.7);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 10000;
}

.confirm-card {
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  transform: scale(1);
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.confirm-icon-container {
  width: 60px;
  height: 60px;
}

.white-space-pre-line {
  white-space: pre-line;
}

/* Animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-active .confirm-card {
  animation: scale-up 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

.fade-leave-active .confirm-card {
  animation: scale-down 0.25s ease forwards;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes scale-up {
  from {
    transform: scale(0.9);
  }
  to {
    transform: scale(1);
  }
}

@keyframes scale-down {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(0.9);
  }
}
</style>
