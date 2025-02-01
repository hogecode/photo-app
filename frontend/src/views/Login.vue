//ToDo: firebaseを使ってテスト
//Fix: PCの全画面で細くなるバグを修正
//Fix: なぜかpiniaにユーザー情報が保存さない

<template>
  <v-container class="d-flex" style="min-height: 100vh;" fluid>
    <v-row justify="center" align="center" class="full-height">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="text-h5">ログイン</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="isValid" lazy-validation>
              <v-text-field
                v-model="email"
                label="メールアドレス*"
                type="email"
                :rules="[emailRules.required, emailRules.valid]"
                required
              />
              <v-text-field
                v-model="password"
                label="パスワード*"
                :type="passwordVisible ? 'text' : 'password'"
                :rules="[passwordRules.required, passwordRules.valid]"
                required
                append-icon="mdi-eye"
                @click:append="togglePasswordVisibility"
              />
              <v-btn :disabled="!isValid" @click="login" color="primary" block>ログイン</v-btn>
            </v-form>
            <v-alert v-if="errorMessage" type="error" dismissible>{{ errorMessage }}</v-alert>
            <p style="margin-top: 10px; font-size: 12px;">
              <span v-text="'アカウントをお持ちではありませんか？ '"></span>
              <router-link to="/register">サインアップ</router-link>
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { loginUser } from '@/services/userService';
import { showUserLoggedInMessage, showUserLoginFailedMessage } from '@/services';

const email = ref('');
const password = ref('');
const isValid = ref(false);
const errorMessage = ref<string | null>(null);
const passwordVisible = ref(false);  // パスワードの表示/非表示切替フラグ
const router = useRouter();

// バリデーションルール
const emailRules = {
  required: (v: string) => !!v || 'メールアドレスは必須です',
  valid: (v: string) => /.+@.+\..+/.test(v) || '正しいメールアドレスを入力してください',
};

const passwordRules = {
  required: (v: string) => !!v || 'パスワードは必須です',
  valid: (v: string) => v.length >= 6 || 'パスワードは6文字以上で入力してください',
};

// パスワード表示/非表示切り替え
const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
};

// ユーザー登録処理
const login = async () => {
  const success = await loginUser(email, password, errorMessage);

  // ログインが成功した場合のみリダイレクト
  if (success) {
    router.push('/');
    showUserLoggedInMessage();
  } else {
    // ログイン失敗時の処理
    console.log(errorMessage.value);
  }
};
</script>

<style scoped lang="scss">
.v-btn {
  margin-top: 5px;
}

.v-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.v-text-field {
  margin-bottom: 10px;
}

.v-card {
  padding: 15px;
  // background-color: #f9f9f9af;
}

.v-alert {
  margin-top: 5px;
}

.v-container {
  max-width: 800px;
  margin: 0 auto;
}

.v-row {
  justify-content: center;
}
</style>
