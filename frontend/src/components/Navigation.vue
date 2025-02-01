//ToDo: v-navigation-drawerがなぜか表示されないのでv-menuで代替

<template>
   <!-- ハンバーメニュー -->
   <v-btn icon @click="toggleDrawer">
    <v-icon>mdi-menu</v-icon>
  </v-btn>

  <!-- メニュー -->
  <v-menu v-model="drawer" :close-on-content-click="false" offset-y>
    <template #activator>
    </template>

    <!-- サイドメニュー -->
    <v-list>
      <v-list-item
        v-for="item in menuItems"
        :key="item.name"
        @click="navigateTo(item.link)"
        @mouseover="showTooltip(item.name)"
        @mouseleave="hideTooltip"
      >
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title v-if="isHovered === item.name"style="color:black">{{ item.name }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router"; // Vue Routerをインポート

// サイドバーの表示状態
const drawer = ref(false);

// ホバー時の状態
const isHovered = ref<string | null>(null);

// メニューアイテム
const menuItems = ref([
  { name: "Home", icon: "mdi-home", link: "/" },
  { name: "Favorite", icon: "mdi-heart", link: "/favorite" },
  { name: "Album", icon: "mdi-album", link: "/albums" },
  { name: "Trash", icon: "mdi-delete", link: "/trash" },
]);

const toggleDrawer = () => {
  drawer.value = !drawer.value;
};

// ホバー時に説明を表示
const showTooltip = (name: string) => {
  isHovered.value = name;
};

// ホバー解除時
const hideTooltip = () => {
  isHovered.value = null;
};

// Vue Routerのインスタンスを取得
const router = useRouter();

// クリック時にページ遷移を行うメソッド
const navigateTo = (link: string) => {
  router.push(link); // Vue Routerを使ってページ遷移
};
</script>

<style scoped lang="scss">
/* サイドバーのカスタムスタイル */
.v-navigation-drawer {
  background-color: #AAAAAA;
  width: 80px !important;
}

.v-list-item-title {
  color: #fff;
  font-size: 14px;
  margin-left: 10px;
}

/* ホバー時の説明をサイドバー内に表示 */
.v-list-item {
  transition: all 0.3s ease;
}

.v-list-item-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.v-list-item:hover {
  background-color: aliceblue;
}

.v-list-item-icon {
  min-width: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.v-list-item-content {
  padding-left: 10px;
}

/* ホバー時の説明 */
.v-list-item-title {
  display: block;
}
</style>
