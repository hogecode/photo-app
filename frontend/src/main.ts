//ToDo: サービスワーカー登録
//ToDo: リファクタリング

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import pinia from "./stores";
import "@/assets/index.css"
import "@/assets/index.scss"
import { getIdToken, onAuthStateChanged } from "firebase/auth";
import { useUserStore } from "./stores/UserStore";
import { auth } from "./firebaseConfig";


// Firebase の認証状態の監視
onAuthStateChanged(auth, (user) => {
  const userStore = useUserStore();

  if (user) {
    // ユーザーがログインしている場合、トークンを取得
    getIdToken(user, true)  // `true` を指定してトークンを強制的にリフレッシュ
      .then((idToken) => {
        userStore.setUser(user, idToken);  // ユーザー情報と ID トークンを Pinia ストアに保存
      })
      .catch((error) => {
        console.error('Error getting ID token:', error);
      });
  } else {
    // ログインしていない場合、ストアをクリア
    userStore.logout();
  }
});

loadFonts();

createApp(App)
.use(router)
.use(vuetify)
.use(pinia)
.mount("#app");
