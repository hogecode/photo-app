//ToDo: エラーリトライなどもいずれ追加
//ToDo: いずれはaxiosに変更する

import { useUserStore } from '@/stores/UserStore';
import { Ref } from 'vue';

/**
 * カスタムfetch関数
 * JSONに対応、デフォルトURL指定
 * 
 * @param url - リクエストを送るAPIエンドポイントのURL
 * @param options - Fetchのオプション（メソッド、ヘッダーなど）
 * @returns レスポンスのデータ
 * 
 * @example
 * async function getUserInfo() {
 *  try {
 *   const userInfo = await useFetch<{ name: string, email: string }>('/user/info');
 *   console.log(userInfo);
 * } catch (error) {
 *   console.error('Error fetching user info:', error);
 * }
 *}
 * 
 * @throws エラーハンドリング: レスポンスが正常でない場合、エラーを投げます
 */
export async function useFetch<T>(url: string, options: RequestInit = {}): Promise<T> {
  // ユーザーストアからIDトークンを取得
  const userStore = useUserStore();
  const idToken = userStore.idToken;

  // サーバーURLを環境変数から取得
  const serverUrl = process.env.VUE_APP_SERVER_URL || 'http://localhost:8000';

  // リクエストURLを組み立て
  const requestUrl = `${serverUrl}${url}`;

  // Fetchオプションにデフォルトのヘッダーを追加
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(idToken && { 'Authorization': `Bearer ${idToken}` }), // IDトークンがあればAuthorizationヘッダーに追加
  };

      // Memo: FormDataの場合はContent-Typeを設定しない
      // Memo: multipart/form-dataの場合エラーになる
      // Memo: これを外すとJSONで送られて422エラーになる
       if (options.body instanceof FormData) {
        delete headers['Content-Type'];  // FormDataの場合、Content-Typeは削除
     }

  // カスタムオプションをマージ
  const mergedOptions: RequestInit = {
    ...options,
    headers: {
      ...headers,
      ...options.headers,
    },
  };

  // Fetchリクエストを送信
  const response = await fetch(requestUrl, mergedOptions);

  // レスポンスが正常でない場合はエラーを投げる
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Request failed');
  }

  // JSONレスポンスを返す
  const data: T = await response.json();
  return data;
}