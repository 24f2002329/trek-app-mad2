import { reactive } from 'vue';

export const confirmState = reactive({
  show: false,
  title: 'Confirmation',
  message: '',
  resolve: null,
  reject: null,
  confirmText: 'Confirm',
  cancelText: 'Cancel',
  isDanger: false
});

export const confirmService = {
  ask(message, options = {}) {
    confirmState.title = options.title || 'Are you sure?';
    confirmState.message = message;
    confirmState.confirmText = options.confirmText || 'Confirm';
    confirmState.cancelText = options.cancelText || 'Cancel';
    confirmState.isDanger = options.isDanger || false;
    confirmState.show = true;

    return new Promise((resolve) => {
      confirmState.resolve = () => {
        confirmState.show = false;
        resolve(true);
      };
      confirmState.reject = () => {
        confirmState.show = false;
        resolve(false);
      };
    });
  }
};

if (typeof window !== 'undefined') {
  window.$confirm = confirmService;
}
