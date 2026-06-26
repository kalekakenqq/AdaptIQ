<script setup>
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();

const links = [
  { to: "/dashboard", label: "Главная", icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 0 0 1 1h3m10-11l2 2m-2-2v10a1 1 0 0 1-1 1h-3m-6 0a1 1 0 0 0 1-1v-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v4a1 1 0 0 0 1 1m-6 0h6" },
  { to: "/analytics", label: "Аналитика", icon: "M9 19v-6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2Zm0 0V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v10m0 0V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v14" },
  { to: "/teacher", label: "Преподавателю", icon: "M12 14l9-5-9-5-9 5 9 5Zm0 0l6.16-3.42A12.08 12.08 0 0 1 21 12c0 3.07-1.34 5.83-3.46 7.71L12 16l-5.54 3.71A12.08 12.08 0 0 1 3 12c0-1.4.32-2.73.84-3.92L12 14Z" },
  { to: "/courses/editor", label: "Курсы", icon: "M12 6.25278C9.92899 4.97965 7.5 4.5 5.5 4.5C4.5 4.5 3.5 4.6 2.5 5V19.5C3.5 19.1 4.5 19 5.5 19C7.5 19 9.92899 19.4797 12 20.7528M12 6.25278C14.071 4.97965 16.5 4.5 18.5 4.5C19.5 4.5 20.5 4.6 21.5 5V19.5C20.5 19.1 19.5 19 18.5 19C16.5 19 14.071 19.4797 12 20.7528M12 6.25278V20.7528" },
  { to: "/profile", label: "Профиль", icon: "M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0ZM12 14a7 7 0 0 0-7 7h14a7 7 0 0 0-7-7Z" },
];
</script>

<template>
  <aside class="sticky top-0 flex h-screen w-60 shrink-0 flex-col bg-card">
    <div class="flex items-center gap-2 px-6 py-6">
      <svg class="h-7 w-7 text-accent-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M9.5 2a3.5 3.5 0 0 0-3.5 3.5v1.05A3.5 3.5 0 0 0 4 9.78v1.69a3 3 0 0 0-1 2.24V16a3 3 0 0 0 3 3h.17A3.5 3.5 0 0 0 9.5 22h1a3.5 3.5 0 0 0 3.43-2.84A3.5 3.5 0 0 0 17 16v-1a3 3 0 0 0-1-2.24V11a3.5 3.5 0 0 0-2-3.16V5.5A3.5 3.5 0 0 0 10.5 2h-1Z" />
      </svg>
      <span class="text-lg font-bold text-text">AdaptIQ</span>
    </div>

    <nav class="flex-1 space-y-1 px-3">
      <router-link
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-text/70 transition-all duration-200 hover:bg-white/5 hover:text-text"
        active-class="bg-accent/15 text-accent-light"
      >
        <svg class="h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path :d="link.icon" />
        </svg>
        {{ link.label }}
      </router-link>
    </nav>

    <div class="flex items-center gap-3 border-t border-white/5 px-6 py-4">
      <div class="flex h-9 w-9 items-center justify-center rounded-full bg-accent/20 text-sm font-semibold text-accent-light">
        {{ (authStore.user?.full_name || "U")[0].toUpperCase() }}
      </div>
      <div class="min-w-0">
        <p class="truncate text-sm font-medium text-text">
          {{ authStore.user?.full_name || "Пользователь" }}
        </p>
        <button class="text-xs text-text/50 hover:text-text/80" @click="authStore.logout()">
          Выйти
        </button>
      </div>
    </div>
  </aside>
</template>
