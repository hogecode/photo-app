
import { useFetch } from '@/hooks/useFetch'; // useFetch関数をインポート
import { useUserStore } from '@/stores/UserStore'; // Piniaストアをインポート
import { Ref } from 'vue';
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut } from 'firebase/auth'; // Firebaseのインポート
import { auth } from '@/firebaseConfig';

export const registerUser = async (
  email: Ref<string>, password: Ref<string>, errorMessage: Ref<string>
) => {
  const userStore = useUserStore(); // Piniaストアの取得

  try {
    errorMessage.value = null;

    // Firebaseでユーザー登録
    const userCredential = await createUserWithEmailAndPassword(auth, email.value, password.value);
    const user = userCredential.user;
    const idToken = await user.getIdToken();  // Firebase IDトークン取得

    // useFetchを使ってサーバーにユーザー登録リクエストを送信
    const response = await useFetch<any>('/api/user/register', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${idToken}`,  // Authorizationヘッダーを追加
        'Content-Type': 'application/json',   // Content-TypeはJSONに設定
      },
      body: JSON.stringify({}),  // bodyは空
    });

    // サーバーからのレスポンスをログに出力
    console.log(response.message); // 例: サーバーから返されたメッセージ

    // Piniaストアにユーザー情報を保存
    userStore.setUser(user, idToken);
    console.log('登録成功', response);

    // Memo: router.pushはvueコンポーネント内に書く必要
  } catch (error) {
    errorMessage.value = '登録に失敗しました。もう一度試してください。';
    console.error('登録エラー:', error.message);
  }
};


// ログイン処理
export const loginUser = async (email: Ref<string>, password: Ref<string>, errorMessage: Ref<string>): Promise<boolean> => {
  const userStore = useUserStore(); // Piniaストアの取得

  try {
    errorMessage.value = null;

    // Firebaseでユーザー認証
    const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value);
    const user = userCredential.user;
    
    // Firebase IDトークンの取得とリフレッシュ
    let idToken = await user.getIdToken();

    // IDトークンの期限が切れている場合、リフレッシュトークンを使用
    try {
      // ここでトークンを再取得
      idToken = await user.getIdToken(true); // `true` にすることでトークンを強制的にリフレッシュ
    } catch (error) {
      console.error("トークンのリフレッシュに失敗しました:", error);
      errorMessage.value = "トークンの取得に失敗しました。再度ログインしてください。";
      return false;
    }

    // Piniaストアにユーザー情報を保存
    userStore.setUser(user, idToken);
    console.log('ログイン成功');

    // ログイン成功
    return true;
  } catch (error) {
    errorMessage.value = 'ログインに失敗しました。もう一度試してください。';
    console.error('ログインエラー:', error.message);
    
    // ログイン失敗
    return false;
  }
};


// ログアウト処理
export const logoutUser = async (errorMessage: Ref<string>) => {
  const userStore = useUserStore(); // Piniaストアの取得

  try {
    errorMessage.value = null;

    // Firebaseでログアウト
    await signOut(auth);
    
    // Piniaストアのユーザー情報をリセット
    userStore.logout();

    console.log('ログアウト成功');
  } catch (error) {
    errorMessage.value = 'ログアウトに失敗しました。もう一度試してください。';
    console.error('ログアウトエラー:', error.message);
  }
};