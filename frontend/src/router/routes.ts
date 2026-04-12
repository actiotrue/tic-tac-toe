export default [
  {
    path: "/",
    name: "home",
    component: () => import("@/pages/home.vue"),
  },
  {
    path: "/game",
    name: "game",
    component: () => import("@/pages/game.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/profile/me",
    name: "profile-me",
    component: () => import("@/pages/profile.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/profile/:userId",
    name: "profile-user",
    component: () => import("@/pages/profile.vue"),
  },
];
