import { createPinia } from "pinia";
import { createApp } from "vue";
import Vue3Toastify, { toast } from "vue3-toastify";

import App from "./App.vue";
import router from "./router";
import "vue3-toastify/dist/index.css";

import { useAuth } from "./store/auth.store";

const pinia = createPinia();
const app = createApp(App);

app.use(pinia);
app.use(router);
app.use(Vue3Toastify, {
  position: toast.POSITION.TOP_CENTER,
  duration: 3000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: true,
  closeButton: "button",
});

const authStore = useAuth();

authStore.initAuth().finally(() => {
  app.mount("#app");
});
