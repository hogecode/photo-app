
import { createPinia } from 'pinia';
import piniaPersistedState from 'pinia-plugin-persistedstate';

const pinia = createPinia();

// Piniaに永続化プラグインを追加
pinia.use(piniaPersistedState);

export default pinia;
