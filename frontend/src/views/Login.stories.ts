import { defineComponent, ref } from 'vue';
import { Meta, StoryFn } from '@storybook/vue3';
import LoginForm from './LoginForm.vue'; // LoginForm.vueのパスを調整

export default {
  title: 'Components/LoginForm', // ストーリーのタイトル
  component: LoginForm,
} as Meta;

const Template: StoryFn = (args: any) => ({
  components: { LoginForm },
  setup() {
    const email = ref('');
    const password = ref('');
    const isValid = ref(false);
    const errorMessage = ref(null);

    // バリデーションルール
    const emailRules = {
      required: (v: any) => !!v || 'メールアドレスは必須です',
      valid: (v: any) => /.+@.+\..+/.test(v) || '正しいメールアドレスを入力してください',
    };

    const passwordRules = {
      required: (v: any) => !!v || 'パスワードは必須です',
      valid: (v: any) => v.length >= 6 || 'パスワードは6文字以上で入力してください',
    };

    // ログイン処理
    const login = async () => {
      errorMessage.value = null;
      try {
        // ここにFirebase認証などの処理を実装
        console.log('ログイン成功');
      } catch (error) {
        errorMessage.value = 'ログインに失敗しました。もう一度試してください。';
        console.error('ログインエラー:', error.message);
      }
    };

    return {
      email,
      password,
      isValid,
      errorMessage,
      emailRules,
      passwordRules,
      login,
    };
  },
  template: '<LoginForm :email="email" :password="password" :isValid="isValid" :errorMessage="errorMessage" :emailRules="emailRules" :passwordRules="passwordRules" @login="login" />',
});

export const Default = Template.bind({});
Default.args = {};
