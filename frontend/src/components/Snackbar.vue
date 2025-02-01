
<template>
  <v-snackbar v-model="snackbarStore.showSnackbar" timeout="3000" bottom left>
    {{ snackbarStore.message }}
    <template #action="{ attrs }">
      <v-btn color="pink" text v-bind="attrs" @click="snackbarStore.hideSnackbar">Close</v-btn>
    </template>
  </v-snackbar>
</template>

<script setup >
import { useSnackbarStore } from '@/stores/SnackbarStore';

// Pinia ストアのインスタンスを取得
const snackbarStore = useSnackbarStore();

</script>
