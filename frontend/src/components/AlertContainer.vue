<template>
  <div class="alert-container position-fixed top-0 end-0 p-3" style="z-index: 9999; max-width: 400px; width: 100%;">
    <transition-group name="alert-list" tag="div">
      <div
        v-for="alert in alerts"
        :key="alert.id"
        class="toast-alert d-flex flex-column mb-3 border rounded-3 shadow-lg overflow-hidden position-relative"
        :class="alertClass(alert.type)"
        role="alert"
      >
        <div class="d-flex align-items-center p-3">
          <!-- Icon -->
          <div class="alert-icon-container me-3 d-flex align-items-center justify-content-center rounded-circle" :class="iconBgClass(alert.type)">
            <i class="bi fs-5" :class="alertIcon(alert.type)"></i>
          </div>
          
          <!-- Message -->
          <div class="flex-grow-1 text-light fw-medium small pe-2">
            {{ alert.message }}
          </div>
          
          <!-- Close button -->
          <button 
            type="button" 
            class="btn-close btn-close-white ms-auto border-0 p-1 opacity-75 hover-opacity-100" 
            @click="dismiss(alert.id)"
            aria-label="Close"
          ></button>
        </div>
        
        <!-- Animated timer bar -->
        <div 
          v-if="alert.duration > 0"
          class="alert-progress-bar position-absolute bottom-0 start-0" 
          :class="progressBarClass(alert.type)"
          :style="{ animationDuration: alert.duration + 'ms' }"
        ></div>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { alertState, alertService } from '../services/alert';

export default {
  name: 'AlertContainer',
  computed: {
    alerts() {
      return alertState.alerts;
    }
  },
  methods: {
    dismiss(id) {
      alertService.dismiss(id);
    },
    alertClass(type) {
      return 'alert-' + (type || 'info');
    },
    iconBgClass(type) {
      return 'icon-' + (type || 'info');
    },
    alertIcon(type) {
      switch (type) {
        case 'success': return 'bi-check-circle-fill';
        case 'danger': return 'bi-exclamation-octagon-fill';
        case 'warning': return 'bi-exclamation-triangle-fill';
        case 'info':
        default:
          return 'bi-info-circle-fill';
      }
    },
    progressBarClass(type) {
      return 'progress-' + (type || 'info');
    }
  }
}
</script>

<style scoped>
.toast-alert {
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Success Styles */
.alert-success {
  background: rgba(34, 197, 94, 0.08) !important;
  border-color: rgba(34, 197, 94, 0.25) !important;
}
.icon-success {
  background: rgba(34, 197, 94, 0.2) !important;
  color: #4ade80 !important;
}
.progress-success {
  background: #22c55e !important;
}

/* Danger Styles */
.alert-danger {
  background: rgba(239, 68, 68, 0.08) !important;
  border-color: rgba(239, 68, 68, 0.25) !important;
}
.icon-danger {
  background: rgba(239, 68, 68, 0.2) !important;
  color: #f87171 !important;
}
.progress-danger {
  background: #ef4444 !important;
}

/* Warning Styles */
.alert-warning {
  background: rgba(234, 179, 8, 0.08) !important;
  border-color: rgba(234, 179, 8, 0.25) !important;
}
.icon-warning {
  background: rgba(234, 179, 8, 0.2) !important;
  color: #facc15 !important;
}
.progress-warning {
  background: #eab308 !important;
}

/* Info Styles */
.alert-info {
  background: rgba(6, 182, 212, 0.08) !important;
  border-color: rgba(6, 182, 212, 0.25) !important;
}
.icon-info {
  background: rgba(6, 182, 212, 0.2) !important;
  color: #22d3ee !important;
}
.progress-info {
  background: #06b6d4 !important;
}

.alert-icon-container {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.btn-close-white {
  filter: invert(1) grayscale(100%) brightness(200%);
  font-size: 0.75rem;
  background-size: 0.75rem;
}

.hover-opacity-100:hover {
  opacity: 1 !important;
}

/* Progress bar animation */
.alert-progress-bar {
  height: 3px;
  width: 100%;
  animation-name: progress-drain;
  animation-timing-function: linear;
  animation-fill-mode: forwards;
}

@keyframes progress-drain {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

/* Vue list animations */
.alert-list-enter-from {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}
.alert-list-enter-to {
  opacity: 1;
  transform: translateX(0) scale(1);
}
.alert-list-leave-from {
  opacity: 1;
  transform: translateX(0) scale(1);
}
.alert-list-leave-to {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}
.alert-list-leave-active {
  position: absolute;
  width: 100%;
}
.alert-list-move {
  transition: transform 0.4s ease;
}
</style>
