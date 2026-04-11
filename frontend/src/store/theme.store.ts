import { defineStore } from "pinia";
import { ref, watch } from "vue";

export const useTheme = defineStore("theme", () => {
  const theme = ref<string>(
    localStorage.getItem("theme")
    || document.documentElement.getAttribute("data-theme")
    || "light",
  );

  const toggleTheme = () => {
    theme.value = theme.value === "dark" ? "light" : "dark";
  };

  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

  mediaQuery.addEventListener("change", (e) => {
    if (!localStorage.getItem("theme")) {
      document.documentElement.setAttribute(
        "data-theme",
        e.matches ? "dark" : "light",
      );
    }
  });

  watch(theme, (val) => {
    localStorage.setItem("theme", val);
    document.documentElement.setAttribute("data-theme", val);
  });

  return {
    theme,
    toggleTheme,
  };
});
