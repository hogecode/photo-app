//ToDo: 検索機能を追加(ホバーで入力形式)
//ToDo: アイコンクリックでホーム画面に遷移
//ToDo: ファイルアップロード機能追加

<template>
  <v-app-bar app>
    <v-row align="center" no-gutters>
      <!-- Navigation Component -->
      <v-col class="d-flex" align="center">
        <Navigation />

        <v-img src="@/assets/app-logo.svg" alt="App Logo" max-width="50px" />

        <!-- 検索バー -->
        <v-text-field
          v-model="searchQuery"
          label="Search"
          solo
          append-icon="mdi-magnify"
          class="icon-input"
        />
      </v-col>

      <v-spacer></v-spacer>

      <!-- ファイルアップロード -->
      <v-col class="d-flex justify-end" align="center">
        <v-file-input
          v-model="file"
          accept="image/*"
          class="icon-input"
          label="select file"
          @change="handleFileChange"
        >
        </v-file-input>

        <!-- Firebase Authから取得したユーザーアイコン -->
        <v-avatar>
          <v-img :src="userPhotoUrl" alt="User Avatar" />
        </v-avatar>
      </v-col>
    </v-row>
  </v-app-bar>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/UserStore";
import Navigation from "./Navigation.vue";
import { uploadFile } from '@/services/fileService';
import { showImageUploadedFailedMessage, showImageUploadedMessage } from "@/services";

// Firebase Authから取得したユーザー情報
const userStore = useUserStore();
const searchQuery = ref("");
const file = ref<File | null>(null);

// Firebase Authからのユーザー画像URL
const userPhotoUrl = ref<string>("");

// ファイルが選択された時に呼ばれる関数
const handleFileChange = () => {
  if (file.value) {
    // ファイルが選択されていればアップロード
    uploadFile(file.value)
      .then(() => {
        console.log('ファイルアップロード完了');
        showImageUploadedMessage();
      })
      .catch((error) => {
        console.error('ファイルアップロードエラー:', error);
        showImageUploadedFailedMessage();
      });
  }
};

onMounted(() => {
  const userStore = useUserStore(); // storeからユーザー情報を取得

  // photoURL がない場合はデフォルト画像を設定
  userPhotoUrl.value =
    userStore.user.photoURL || require("@/assets/app-logo.svg");
});
</script>

<style scoped lang="scss">
.v-app-bar {
  background-color: #1976d2;
}

.v-row {
  justify-content: flex-between;
  align-items: center;
}

.v-text-field {
  min-width:250px;
  max-width: 350px;
}

.v-avatar {
  width: 40px;
  height: 40px;
}

.v-file-input {
  min-width: 150px;
  max-width: 350px;
}

.icon-input .v-input__append-inner,
.icon-input .v-input__prepend-inner {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
