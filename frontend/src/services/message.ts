
import { useSnackbarStore } from '@/stores/SnackbarStore';

// Pinia ストアのインスタンスを取得
const snackbarStore = useSnackbarStore();

// **画像関連のメッセージ(showImage)**
// 画像を作成したときのメッセージ
export const showImageUploadedMessage = () => {
  snackbarStore.showMessage('画像のアップロードに成功しました！');
};

// ユーザーがログインに失敗したときのメッセージ
export const showImageUploadedFailedMessage = () => {
  snackbarStore.showMessage('画像のアップロードに失敗しました。');
};

// 画像を更新したときのメッセージ
export const showImageUpdatedMessage = () => {
  snackbarStore.showMessage('画像が正常に更新されました！');
};

// 画像を削除したときのメッセージ
export const showImageDeletedMessage = () => {
  snackbarStore.showMessage('画像が正常に削除されました！');
};


// **ユーザー関連のメッセージ(showUser)**
// ユーザーが正常にログインしたときのメッセージ
export const showUserLoggedInMessage = () => {
  snackbarStore.showMessage('ログインに成功しました！');
};

// ユーザーがログインに失敗したときのメッセージ
export const showUserLoginFailedMessage = () => {
  snackbarStore.showMessage('ログインに失敗しました。ユーザー名またはパスワードが間違っています。');
};

// ユーザーが正常にログアウトしたときのメッセージ
export const showUserLoggedOutMessage = () => {
  snackbarStore.showMessage('ログアウトしました。');
};

// ユーザーが正常にアカウントを登録したときのメッセージ
export const showUserRegisteredMessage = () => {
  snackbarStore.showMessage('アカウントが正常に作成されました！');
};

// ユーザーがログインに失敗したときのメッセージ
export const showUserRegisteredFailedMessage = () => {
  snackbarStore.showMessage('ログインに失敗しました。ユーザー名またはパスワードが間違っています。');
};

// ユーザーが正常にアカウントを削除したときのメッセージ
export const showUserDeletedMessage = () => {
  snackbarStore.showMessage('アカウントが正常に削除されました。');
};


// **汎用メッセージ**
// エラーメッセージ
export const showErrorMessage = (error: string) => {
  snackbarStore.showMessage(`エラー: ${error}`);
};

// 他のカスタムメッセージ
export const showCustomMessage = (message: string) => {
  snackbarStore.showMessage(message);
};
