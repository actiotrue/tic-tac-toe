import { createRouter, createWebHistory } from "vue-router";

import { useAuth } from "@/store/auth.store";

import routes from "./routes";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to) => {
  const authStore = useAuth();
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return "/?modal=auth&method=login";
  }
  return true;
});

export default router;
