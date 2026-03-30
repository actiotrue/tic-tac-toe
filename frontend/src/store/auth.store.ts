import { defineStore } from "pinia";
import { ref } from "vue";

import * as authApi from "@/api/auth";

export const useAuth = defineStore("auth", () => {
  const isLoggedIn = ref<boolean>(localStorage.getItem("accessToken") !== null);
  const isLoading = ref<boolean>(false);
  const userId = ref<string | null>(null);

  const signup = async (username: string, password: string) => {
    isLoading.value = true;
    try {
      await authApi.signup(username, password);
    }
    finally {
      isLoading.value = false;
    }
  };

  const login = async (username: string, password: string) => {
    isLoading.value = true;
    try {
      const response = await authApi.login(username, password);
      localStorage.setItem("accessToken", response.accessToken);
      isLoggedIn.value = true;
      userId.value = response.userId;
    }
    finally {
      isLoading.value = false;
    }
  };

  const initAuth = async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      return;
    }
    isLoading.value = true;
    try {
      const response = await authApi.getMe();
      isLoggedIn.value = true;
      userId.value = response.id;
    }
    finally {
      isLoading.value = false;
      authApi.logout();
    }
  };

  const logout = async () => {
    isLoading.value = true;
    try {
      await authApi.logout();
      localStorage.removeItem("accessToken");
      isLoggedIn.value = false;
      userId.value = null;
    }
    finally {
      isLoading.value = false;
    }
  };

  return {
    isLoggedIn,
    isLoading,
    userId,
    signup,
    login,
    initAuth,
    logout,
  };
});
