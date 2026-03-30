import { defineStore } from "pinia";
import { ref, watch } from "vue";

export const useTheme = defineStore("theme", () => {
  const theme = ref<string>(localStorage.getItem("theme") || "dark");

  const toggleTheme = () => {
    theme.value = theme.value === "dark" ? "light" : "dark";
  };

  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

  const updateFromSystem = () => {
    if (!localStorage.getItem("color-scheme")) {
      theme.value = mediaQuery.matches ? "dark" : "light";
    }
  };

  mediaQuery.addEventListener("change", updateFromSystem);

  watch(
    theme,
    () => {
      localStorage.setItem("theme", theme.value);
      document.documentElement.style.colorScheme = theme.value;
    },
    { immediate: true },
  );

  return {
    theme,
    toggleTheme,
  };
});
