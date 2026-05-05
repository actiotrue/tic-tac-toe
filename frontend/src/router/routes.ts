export default [
  {
    path: "/",
    name: "home",
    component: () => import("@/pages/home.vue"),
  },
  {
    path: "/game",
    component: () => import("@/pages/game.vue"),
    children: [
      {
        path: "ai",
        name: "game-ai",
        component: () => import("@/pages/game.vue"),
        meta: { requiresAuth: false },
      },
      {
        path: "player",
        name: "game-player",
        component: () => import("@/pages/game.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "spectate",
        name: "game-spectate",
        component: () => import("@/pages/game.vue"),
        meta: { requiresAuth: false },
      },
    ],
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
