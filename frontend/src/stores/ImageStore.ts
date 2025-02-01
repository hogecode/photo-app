/**
 * 画像一覧と選択中の画像を保存するストア
 */

import { defineStore } from 'pinia';
import { ref } from 'vue';

// 画像情報の型定義
// Memo: idが数値か文字列か
interface Image {
  id: string;
  url: string;
  title: string;
}

export const useImageStore = defineStore('imageStore', {
  // ステート: 画像リストと選択中の画像を保持
  state: () => ({
    imageList: [] as Image[], // 画像リスト
    selectedImage: null as Image | null, // 選択中の画像
  }),

  // アクション: 画像リストや選択画像を操作
  actions: {
    // 画像リストを設定
    setImageList(images: Image[]) {
      this.imageList = images;
    },
    
    // 選択中の画像を設定
    setSelectedImage(image: Image) {
      this.selectedImage = image;
    },
    
    // 画像を追加
    addImage(image: Image) {
      this.imageList.push(image);
    },
    
    // 画像を削除
    removeImage(id: string) {
      this.imageList = this.imageList.filter(image => image.id !== id);
    },
  },

  // Pinia Persist プラグイン設定
  persist: {
    key: 'image_store', // 保存するキーをカスタマイズ
    storage: localStorage, // localStorage または sessionStorage を選択
  },
});
