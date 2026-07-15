import { reactive } from 'vue';

export const alertState = reactive({
  alerts: []
});

let alertId = 0;

export const alertService = {
  show(message, type = 'info', duration = 4000) {
    const id = ++alertId;
    alertState.alerts.push({ id, message, type, duration });
    if (duration > 0) {
      setTimeout(() => {
        this.dismiss(id);
      }, duration);
    }
    return id;
  },
  success(message, duration = 4000) {
    return this.show(message, 'success', duration);
  },
  error(message, duration = 4000) {
    return this.show(message, 'danger', duration);
  },
  info(message, duration = 4000) {
    return this.show(message, 'info', duration);
  },
  warning(message, duration = 4000) {
    return this.show(message, 'warning', duration);
  },
  dismiss(id) {
    const index = alertState.alerts.findIndex(a => a.id === id);
    if (index !== -1) {
      alertState.alerts.splice(index, 1);
    }
  }
};

if (typeof window !== 'undefined') {
  window.$alerts = alertService;
}
