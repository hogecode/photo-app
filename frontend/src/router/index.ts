
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { useUserStore } from "@/stores/UserStore";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: () => import('@/views/Home.vue'),
  },
{
  path: "/login",
  name: "Login",
  component: () => import('@/views/Login.vue'),
},
{
  path: "/register",
  name: "Register",
  component: () => import('@/views/Register.vue'),
},
{ path: '/image/:id', 
  name: 'ImageDetail', 
  component: () => import('@/views/ImageDetail.vue'), 
  props: true },
{
  path: '/:pathMatch(.*)*',
  name: 'NotFound',
  component: () => import('@/views/NotFound.vue'),
},
];

const router = createRouter({
  // ルーティングのベース URL
  history: createWebHistory(process.env.BASE_URL),
  routes,
      // ページ遷移時のスクロールの挙動の設定
      scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            // 戻る/進むボタンが押されたときは保存されたスクロール位置を使う
            return savedPosition;
        } else {
            // それ以外は常に先頭にスクロールする
            return {top: 0, left: 0};
        }
    }
});


// 認証チェックのナビゲーションガード
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();

  // 認証されていない場合、/login または /register 以外のルートにアクセスできない
  if (!userStore.user && (to.path !== '/login' && to.path !== '/register')) {
    // ログインしていない場合、ログインページにリダイレクト
    next('/login');
  } else {
    // 認証されている場合、またはログインページ/登録ページにアクセスしている場合はそのまま遷移
    next();
  }
});


export default router;
