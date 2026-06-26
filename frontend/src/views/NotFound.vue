<script setup>
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
</script>

<template>
  <div class="flex min-h-screen flex-col items-center justify-center bg-bg px-4 text-center">
    <div class="mb-6 flex items-center gap-2">
      <svg
        class="h-9 w-9 text-accent-light"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
      >
        <path
          d="M9.5 2a3.5 3.5 0 0 0-3.5 3.5v1.05A3.5 3.5 0 0 0 4 9.78v1.69a3 3 0 0 0-1 2.24V16a3 3 0 0 0 3 3h.17A3.5 3.5 0 0 0 9.5 22h1a3.5 3.5 0 0 0 3.43-2.84A3.5 3.5 0 0 0 17 16v-1a3 3 0 0 0-1-2.24V11a3.5 3.5 0 0 0-2-3.16V5.5A3.5 3.5 0 0 0 10.5 2h-1Z"
        />
      </svg>
      <span class="text-2xl font-bold text-text">AdaptIQ</span>
    </div>

    <h1 class="bg-gradient-to-r from-accent to-accent-light bg-clip-text text-7xl font-extrabold text-transparent">
      404
    </h1>
    <p class="mt-4 text-lg text-text/70">Страница не найдена</p>
    <p class="mt-1 text-sm text-text/40">Возможно, она была перемещена или никогда не существовала.</p>

    <router-link
      :to="authStore.isAuthenticated ? '/dashboard' : '/login'"
      class="mt-8 rounded-xl bg-gradient-to-r from-accent to-accent-light px-6 py-2.5 font-medium text-white shadow-lg transition-all duration-200 hover:brightness-110"
    >
      На главную
    </router-link>
  </div>
</template>
