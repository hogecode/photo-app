
<template>
  <v-app>
    <v-main id="app">
      <router-view />
      <Snackbar />
    </v-main>
  </v-app>
</template>

<script setup>
import Snackbar from '@/components/Snackbar.vue';
import Navigation from '@/components/Navigation.vue';

/*
import { onMounted, ref, watch } from 'vue'

// ダークモード設定を保持するためのref
const darkMode = ref(window.matchMedia('(prefers-color-scheme: dark)').matches)

// ダークモードの変更を監視
const updateTheme = (e) => {
  darkMode.value = e.matches
}

// Vuetifyのテーマを更新するための方法
const updateVuetifyTheme = () => {
  // Vuetifyのテーマを更新
  if (darkMode.value) {
    // ダークモード
    document.documentElement.setAttribute('data-theme', 'dark')
    this.$vuetify.theme.dark = true
  } else {
    // ライトモード
    document.documentElement.removeAttribute('data-theme')
    this.$vuetify.theme.dark = false
  }
}

// 初期設定とイベントリスナーの登録
onMounted(() => {
  // 初回のテーマ設定を更新
  updateVuetifyTheme()

  // prefers-color-scheme の変更を監視
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateTheme)
})

// darkModeが変更された場合にVuetifyテーマを更新
watch(darkMode, () => {
  updateVuetifyTheme()
})
  */
</script>

<style lang="scss">

// ブラウザのデフォルトスタイルの上書き
// 選択時の色
*::selection {
	background-color: #E64F9780;
}

// リンクの既定の CSS をリセット
a, a:link, a:visited, a:hover, a:active {
    color: inherit;
    text-decoration: none;
}


// 全体のスタイル
html {
    overflow-y: auto !important;
    touch-action: manipulation;
}

// ヘッダー以外のメインコンテンツのルート
body main {
    display: flex;
    width: 100%;
    min-height: 100%;
}


// カーソルをポインターにする
.cursor-pointer {
    cursor: pointer;
}

</style>
