export default [
  {
    path: "/",
    name: "Home",
    component: () => import("@/pages/home.vue"),
  },
  {
    path: "/game",
    name: "Game",
    component: () => import("@/pages/game.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/profile",
    name: "Profile",
    component: () => import("@/pages/profile.vue"),
    meta: {
      requiresAuth: true,
    },
  },
];
