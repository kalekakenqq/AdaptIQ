<script setup>
import { useAuthStore } from "../stores/auth";

defineProps({
  title: {
    type: String,
    default: "",
  },
});

const authStore = useAuthStore();
</script>

<template>
  <header class="flex items-center justify-between border-b border-white/5 bg-bg px-6 py-4">
    <h1 class="text-lg font-semibold text-text">{{ title }}</h1>

    <div class="flex items-center gap-3">
      <span class="text-sm text-text/70">{{ authStore.user?.full_name || "Пользователь" }}</span>
      <div
        class="flex h-9 w-9 items-center justify-center rounded-full bg-accent/20 text-sm font-semibold text-accent-light"
      >
        {{ (authStore.user?.full_name || "U")[0].toUpperCase() }}
      </div>
    </div>
  </header>
</template>
