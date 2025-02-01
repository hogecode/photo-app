//ToDo: 画像が変わったらURLは変更
//ToDo: router.push('/');で戻るボタンを追加

<template>
  <v-container class="container">
      <Header/>
    <!-- 画像表示部分：上下中央に配置し、横一杯に表示 -->
    <v-row class="d-flex justify-center align-center">
      <v-col cols="12" class="d-flex justify-center">
        <v-img
          :src="imageUrl"
          alt="Image to crop"
          ref="image"
          class="image-cropper"
        />
      </v-col>
    </v-row>

    <!-- 前後画像移動ボタン：アイコンを使用 -->
    <v-row class="mt-4">
      <v-col cols="6" class="d-flex justify-start">
        <v-btn
          @click="moveImage('prev')"
          icon
          color="primary"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-col>
      <v-col cols="6" class="d-flex justify-end">
        <v-btn
          @click="moveImage('next')"
          icon
          color="primary"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <!-- トリミングボタン：一番下に配置 -->
    <v-row class="mt-4">
      <v-col class="d-flex justify-center">
        <v-btn @click="downloadCroppedImage" color="success">
          トリミングしてダウンロード
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { useImageStore } from '@/stores/ImageStore'; // Piniaストアをインポート
import Cropper from 'cropperjs';
import Header from '@/components/Header.vue';

// Piniaストアから選択された画像情報を取得
const imageStore = useImageStore();
const imageUrl = ref<string>(''); // 表示する画像のURL
const cropperInstance = ref<Cropper | null>(null); // Cropperインスタンス

// 画像URLの設定とCropper.jsの初期化
const fetchImage = () => {
  const selectedImage = imageStore.selectedImage;
  if (selectedImage) {
    imageUrl.value = selectedImage.url; // URLを設定
    console.log("Selected Image URL:", imageUrl.value); // ログを出力して確認

    // VueのnextTickを使用して、DOMが更新された後にCropperを初期化
    nextTick(() => {
      const imageElement = document.querySelector('img') as HTMLImageElement;
      if (imageElement && !cropperInstance.value) {
        cropperInstance.value = new Cropper(imageElement, {
          aspectRatio: 16 / 9,
          viewMode: 1,
          autoCropArea: 0.8,
          movable: true,
          scalable: true,
          zoomable: true,
          rotatable: true,
        });
      }
    });
  } else {
    console.error("No selected image found");
  }
};

// 前後の画像に移動する処理
const moveImage = (direction: 'prev' | 'next') => {
  const selectedImage = imageStore.selectedImage;
  if (selectedImage) {
    let newIndex = imageStore.imageList.findIndex((image) => image.id === selectedImage.id);
    
    if (direction === 'prev') {
      newIndex -= 1; // 前の画像に移動
    } else if (direction === 'next') {
      newIndex += 1; // 次の画像に移動
    }

    // インデックスが範囲外にならないように調整
    if (newIndex >= 0 && newIndex < imageStore.imageList.length) {
      const nextImage = imageStore.imageList[newIndex];
      imageStore.setSelectedImage(nextImage); // 新しい画像をストアに保存
      fetchImage(); // 新しい画像を読み込む
    }
  }
};

// トリミングした画像をダウンロード
const downloadCroppedImage = () => {
  if (cropperInstance.value) {
    const canvas = cropperInstance.value.getCroppedCanvas();
    const link = document.createElement('a');
    link.href = canvas.toDataURL();
    link.download = 'cropped-image.png';
    link.click();
  }
};

// コンポーネントがマウントされたときに画像を設定
onMounted(() => {
  fetchImage();
});
</script>

<style scoped>
/* 画像を上下中央に配置 */
.container{
  max-height: 100vh;   /* 画面の高さを最大に */
}

.fill-height {
  max-height: 100vh;
}

.image-cropper {
  max-height: 80vh;   /* 画面の高さを最大に */
  max-width: 100%;      /* 横幅を最大に */
  object-fit: contain;  /* 画像の縦横比を保ちながら収める */
}
</style>

