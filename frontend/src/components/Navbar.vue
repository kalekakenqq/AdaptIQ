<script setup>
import { useAuthStore } from "../stores/auth";
import { useThemeStore } from "../stores/theme";

defineProps({
  title: {
    type: String,
    default: "",
  },
});

const authStore = useAuthStore();
const themeStore = useThemeStore();
</script>

<template>
  <header class="flex items-center justify-between border-b border-white/5 bg-bg px-6 py-4">
    <h1 class="text-lg font-semibold text-text">{{ title }}</h1>

    <div class="flex items-center gap-3">
      <button
        class="flex h-9 w-9 items-center justify-center rounded-full bg-white/5 text-text/70 transition-all duration-200 hover:bg-white/10 hover:text-text"
        :title="themeStore.isDark ? 'Светлая тема' : 'Тёмная тема'"
        @click="themeStore.toggle()"
      >
        <svg
          v-if="themeStore.isDark"
          class="h-5 w-5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
        >
          <circle cx="12" cy="12" r="4" />
          <path
            d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32 1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"
          />
        </svg>
        <svg v-else class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z" />
        </svg>
      </button>

      <span class="text-sm text-text/70">{{ authStore.user?.full_name || "Пользователь" }}</span>
      <div
        class="flex h-9 w-9 items-center justify-center rounded-full bg-accent/20 text-sm font-semibold text-accent-light"
      >
        {{ (authStore.user?.full_name || "U")[0].toUpperCase() }}
      </div>
    </div>
  </header>
</template>
