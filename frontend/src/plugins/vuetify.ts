
// Styles
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

// Vuetify
import { createVuetify } from "vuetify";

const dark = window.matchMedia('(prefers-color-scheme: dark)').matches

export default createVuetify({
  theme: {
    defaultTheme: dark ? 'dark' : 'light',
    themes: {
      dark: {
        dark: true,
        colors: {
          background: '#2f2f2f',  // ダークテーマの背景色
          primary: '#bb86fc',     // プライマリカラー
        },
      },
      light: {
        dark: false,
        colors: {
          background: '#fafafa',  // ライトテーマの背景色
          primary: '#6200ea',     // プライマリカラー
        },
      },
    },
  },
})
// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides


