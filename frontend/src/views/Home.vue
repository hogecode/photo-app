//Fix: なぜかタグが閉じられていないエラー 
//ToDo:この画面全体でドラッグドロップで画像を送信を受け付ける

<template>
  <v-container>
    <Header />
    <v-row>
      <!-- 画像一覧(個数はこれでいい)) -->
      <v-col
        v-for="image in imageList"
        :key="image.id"
        :cols="6"
        :sm="6"
        :md="4"
        :lg="3"
      >
        <v-card @click="goToDetail(image.id)" class="pa-0" :hover="true">
          <v-img
            :src="image.url"
            :alt="image.title"
            height="200px"
            class="ma-0"
          >
          </v-img>
          <v-card-title style="font-size: 15px;">{{ image.title }}</v-card-title>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { ref, onMounted, computed } from "vue";
import Header from "@/components/Header.vue";
import { useImageStore } from "@/stores/ImageStore";
import { fetchImageList } from "@/services";

// ルーターインスタンス
const router = useRouter();

// 画像詳細画面へ遷移する関数
const goToDetail = (id: string) => {
  const selectedImage = imageStore.imageList.find(image => image.id === id);
  imageStore.setSelectedImage(selectedImage || null); // 選択した画像を設定
  router.push({ name: "ImageDetail", params: { id } });
};

const imageStore = useImageStore();

// 画像リストを取得してストアに保存
const fetchImages = async () => {
  try {
    const images = await fetchImageList(); // 画像リストを取得
    imageStore.setImageList(images); // 画像リストをストアに保存
  } catch (error) {
    console.error("画像リスト取得失敗:", error);
  }
};

// コンポーネントがマウントされたときに画像データを取得
onMounted(() => {
  fetchImages();
});

// ストアからリアクティブに画像リストを取得
const imageList = computed(() => imageStore.imageList); // `computed` を使用してリアクティブに取得

</script>

<style lang="sass" module></style>
