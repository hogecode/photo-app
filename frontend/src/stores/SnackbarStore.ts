
import { defineStore } from 'pinia';

export const useSnackbarStore = defineStore('snackbar', {
  state: () => ({
    message: '',
    showSnackbar: false,
  }),
  actions: {
    showMessage(message: string) {
      this.message = message;
      this.showSnackbar = true;
      setTimeout(() => {
        this.showSnackbar = false; // 3秒後にスナックバーを非表示にする
      }, 3000);
    },
    hideSnackbar() {
      this.showSnackbar = false; // 手動でスナックバーを非表示にする
    }
  }
});
