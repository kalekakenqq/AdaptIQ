import { defineStore } from "pinia";

const STORAGE_KEY = "adaptiq_theme";

export const useThemeStore = defineStore("theme", {
  state: () => ({
    isDark: localStorage.getItem(STORAGE_KEY) !== "light",
  }),

  actions: {
    apply() {
      document.documentElement.classList.toggle("light", !this.isDark);
    },

    init() {
      this.apply();
    },

    toggle() {
      this.isDark = !this.isDark;
      localStorage.setItem(STORAGE_KEY, this.isDark ? "dark" : "light");
      this.apply();
    },
  },
});
