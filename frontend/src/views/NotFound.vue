
<template>
  <v-container class="not-found-container" fluid>
    <v-row justify="center" align="center" class="height-100">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-center">
            <v-img src="@/assets/404-icon.svg" contain max-height="300"></v-img> <!-- 任意の404画像を使う -->
          </v-card-title>
          <v-card-text class="text-center">
            <h2 class="display-1">404</h2>
            <p>お探しのページは見つかりませんでした。</p>
            <v-btn color="primary" @click="goHome" class="mt-3">ホームに戻る</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

// ホームページへのリダイレクト
const goHome = () => {
  router.push('/');
};
</script>

<style scoped lang="scss">
.not-found-container {
  min-height: 100vh;
}

.v-card {
  padding: 20px;
}

.text-center {
  text-align: center;
}

.display-1 {
  font-size: 5rem;
}

.v-btn {
  font-size: 1.1rem;
  padding: 10px 20px;
}

.v-row {
  min-height: 100vh;
}
</style>
