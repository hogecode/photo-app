//ToDo: ファイル名に注意
//ToDo: authenticatedも追加

// stores/user.js (または user.ts)
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,         // ユーザー情報
    idToken: null,      // IDトークンを追加
  }),
  actions: {
    setUser(user, idToken) {
      this.user = user;
      // Memo: 本当はHTTPSクッキーやredisに保存するべき
      // Memo: XSS対策は必須
      this.idToken = idToken;  // IDトークンを設定
    },
    logout() {
      this.user = null;
      this.idToken = null;  // ログアウト時にIDトークンもクリア
    },
  },
  persist: {
    key: 'user_store', // 保存するキーをカスタマイズ
    storage: localStorage, // localStorage または sessionStorage を選択
  },
});
