//Refactor:
Loginと同じ見た目や機能にしたいので共通scssファイルとvalidate.tsを作成 //ToDo:
出来ればgoogleOauthも追加 //ToDo:
名前とパスワードを送信せず、bodyは空でトークンのみ送信

<template>
  <v-container class="d-flex" style="min-height: 100vh" fluid>
    <v-row justify="center" align="center" class="full-height">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="text-h5">ユーザー登録</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="isValid" lazy-validation>
              <v-text-field
                v-model="email"
                label="メールアドレス*"
                type="email"
                :rules="[emailRules.required, emailRules.valid]"
                required
                persistent-hint
                hint="適当なメールアドレスでいいです"
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
              <v-text-field
                v-model="confirmPassword"
                label="パスワード確認*"
                :type="passwordVisible ? 'text' : 'password'"
                :rules="[
                  confirmPasswordRules.required,
                  confirmPasswordRules.match,
                ]"
                required
                append-icon="mdi-eye"
                @click:append="togglePasswordVisibility"
              />
              <v-btn
                :disabled="!isValid"
                @click="register"
                color="primary"
                block
                >登録</v-btn
              >
            </v-form>
            <v-alert v-if="errorMessage" type="error" dismissible>{{
              errorMessage
            }}</v-alert>
            <p style="margin-top: 10px; font-size: 12px;">
              <span v-text="'すでにアカウントをお持ちですか？ '"></span>
              <router-link to="/login">ログイン</router-link>
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { registerUser } from "@/services/userService";
import { showUserRegisteredFailedMessage, showUserRegisteredMessage } from "@/services";

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const isValid = ref(false);
const errorMessage = ref<string | null>(null);
const passwordVisible = ref(false); // パスワード表示/非表示切替フラグ
const router = useRouter();

// バリデーションルール
//ToDo: 本当はfirebase funcなどでも検証する必要がある
const emailRules = {
  required: (v: string) => !!v || "メールアドレスは必須です",
  valid: (v: string) =>
    /.+@.+\..+/.test(v) || "正しいメールアドレスを入力してください",
};

const passwordRules = {
  required: (v: string) => !!v || "パスワードは必須です",
  valid: (v: string) =>
    v.length >= 6 || "パスワードは6文字以上で入力してください",
};

const confirmPasswordRules = {
  required: (v: string) => !!v || "パスワード確認は必須です",
  match: (v: string) => v === password.value || "パスワードが一致しません",
};

// パスワード表示/非表示切り替え
const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
};

// ユーザー登録処理
const register = async () => {
  // ユーザー登録処理を呼び出す
  await registerUser(email, password, errorMessage);

  // 登録後、ホームページにリダイレクト
  router.push("/");
  
  showUserRegisteredMessage();

  if (errorMessage.value) {
    console.log(errorMessage.value);
    showUserRegisteredFailedMessage();
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
