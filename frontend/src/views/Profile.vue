<script setup>
import axios from "axios";
import { computed, onMounted, ref } from "vue";

import Navbar from "../components/Navbar.vue";
import Sidebar from "../components/Sidebar.vue";
import { useAuthStore } from "../stores/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const authStore = useAuthStore();
const profile = ref(null);
const loading = ref(true);

const roleLabel = computed(() => {
  if (profile.value?.role === "teacher") return "Преподаватель";
  return "Студент";
});

const registeredDate = computed(() => {
  if (!profile.value?.created_at) return "—";
  return new Date(profile.value.created_at).toLocaleDateString("ru-RU");
});

async function loadProfile() {
  loading.value = true;
  try {
    const { data } = await axios.get(`${API_BASE_URL}/users/me`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    });
    profile.value = data;
  } catch (error) {
    console.error("Ошибка загрузки профиля:", error.response?.data ?? error.message);
  } finally {
    loading.value = false;
  }
}

onMounted(loadProfile);
</script>

<template>
  <div class="flex min-h-screen bg-bg">
    <Sidebar />

    <div class="flex-1">
      <Navbar title="Профиль" />

      <main class="space-y-6 p-6">
        <div class="card flex items-center gap-4 p-6">
          <div
            class="flex h-16 w-16 items-center justify-center rounded-full bg-accent/20 text-2xl font-bold text-accent-light"
          >
            {{ (profile?.name || "U")[0].toUpperCase() }}
          </div>
          <div>
            <h2 class="text-xl font-bold text-text">{{ profile?.name || "Пользователь" }}</h2>
            <p class="text-sm text-text/60">{{ roleLabel }}</p>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div class="card p-5">
            <p class="text-sm text-text/60">Email</p>
            <p class="mt-1 truncate font-medium text-text">{{ profile?.email || "—" }}</p>
          </div>
          <div class="card p-5">
            <p class="text-sm text-text/60">Роль</p>
            <p class="mt-1 font-medium text-text">{{ roleLabel }}</p>
          </div>
          <div class="card p-5">
            <p class="text-sm text-text/60">Дата регистрации</p>
            <p class="mt-1 font-medium text-text">{{ registeredDate }}</p>
          </div>
        </div>

        <div>
          <h3 class="mb-3 text-sm font-medium text-text/70">Статистика</h3>
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div class="card p-5">
              <p class="text-sm text-text/60">Всего сессий</p>
              <p class="mt-2 text-2xl font-bold text-accent-light">
                {{ profile?.stats?.sessions_count ?? 0 }}
              </p>
            </div>
            <div class="card p-5">
              <p class="text-sm text-text/60">Средний результат</p>
              <p class="mt-2 text-2xl font-bold text-green-400">
                {{ ((profile?.stats?.avg_score ?? 0) * 100).toFixed(0) }}%
              </p>
            </div>
            <div class="card p-5">
              <p class="text-sm text-text/60">Лучший результат</p>
              <p class="mt-2 text-2xl font-bold text-accent-light">100%</p>
            </div>
          </div>
        </div>

        <button class="btn-primary max-w-xs" :disabled="loading">Редактировать профиль</button>
      </main>
    </div>
  </div>
</template>
