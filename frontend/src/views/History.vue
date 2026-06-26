<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";

import Navbar from "../components/Navbar.vue";
import Sidebar from "../components/Sidebar.vue";
import { useAuthStore } from "../stores/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const authStore = useAuthStore();
const sessions = ref([]);
const loading = ref(true);
const selected = ref(null);

// демо-детализация для модального окна
const demoTimeline = [
  { time: "02:14", count: 1 },
  { time: "05:41", count: 2 },
  { time: "08:03", count: 1 },
  { time: "11:20", count: 3 },
  { time: "14:52", count: 1 },
];
const demoHardQuestions = [
  "Производная сложной функции",
  "Несобственный интеграл",
  "Признак Даламбера для рядов",
];

function formatDate(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleString("ru-RU");
}

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}м ${s}с`;
}

function riskBadge(violations) {
  if (violations <= 1) return "bg-green-500/15 text-green-400";
  if (violations <= 3) return "bg-yellow-500/15 text-yellow-400";
  return "bg-red-500/15 text-red-400";
}

async function loadHistory() {
  loading.value = true;
  try {
    const { data } = await axios.get(`${API_BASE_URL}/sessions/history`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    });
    sessions.value = data;
  } catch (error) {
    console.error("Ошибка загрузки истории:", error.response?.data ?? error.message);
  } finally {
    loading.value = false;
  }
}

onMounted(loadHistory);
</script>

<template>
  <div class="flex min-h-screen bg-bg">
    <Sidebar />

    <div class="flex-1">
      <Navbar title="История сессий" />

      <main class="p-6">
        <div class="card overflow-hidden">
          <table class="w-full text-left text-sm">
            <thead class="bg-white/5 text-text/60">
              <tr>
                <th class="px-5 py-3">Дата</th>
                <th class="px-5 py-3">Курс</th>
                <th class="px-5 py-3">Балл</th>
                <th class="px-5 py-3">Нарушения</th>
                <th class="px-5 py-3">Длительность</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="session in sessions"
                :key="session.id"
                class="cursor-pointer border-t border-white/5 transition-all duration-200 hover:bg-white/5"
                @click="selected = session"
              >
                <td class="px-5 py-3 text-text/80">{{ formatDate(session.date) }}</td>
                <td class="px-5 py-3 text-text">{{ session.course }}</td>
                <td class="px-5 py-3 text-text/80">{{ (session.score * 100).toFixed(0) }}%</td>
                <td class="px-5 py-3">
                  <span :class="['rounded-full px-3 py-1 text-xs font-medium', riskBadge(session.violations)]">
                    {{ session.violations }}
                  </span>
                </td>
                <td class="px-5 py-3 text-text/80">{{ formatDuration(session.duration_seconds) }}</td>
              </tr>
            </tbody>
          </table>

          <p v-if="!loading && sessions.length === 0" class="p-6 text-sm text-text/40">
            История сессий пуста
          </p>
        </div>
      </main>
    </div>

    <div
      v-if="selected"
      class="fixed inset-0 z-40 flex items-center justify-center bg-black/60 p-4"
      @click.self="selected = null"
    >
      <div class="card w-full max-w-lg p-6">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-text">Детали сессии</h3>
          <button class="text-text/50 hover:text-text" @click="selected = null">✕</button>
        </div>

        <p class="text-sm text-text/60">{{ selected.course }} · {{ formatDate(selected.date) }}</p>

        <h4 class="mb-2 mt-5 text-sm font-medium text-text/70">Нарушения по времени</h4>
        <div class="flex h-28 items-end gap-2">
          <div
            v-for="point in demoTimeline"
            :key="point.time"
            class="flex flex-1 flex-col items-center gap-1"
          >
            <div
              class="w-full rounded-t bg-gradient-to-t from-accent to-accent-light"
              :style="{ height: `${point.count * 24}px` }"
            ></div>
            <span class="text-[10px] text-text/40">{{ point.time }}</span>
          </div>
        </div>

        <h4 class="mb-2 mt-5 text-sm font-medium text-text/70">Вопросы с затруднениями</h4>
        <ul class="space-y-1.5">
          <li
            v-for="q in demoHardQuestions"
            :key="q"
            class="flex items-center gap-2 text-sm text-text/70"
          >
            <span class="h-1.5 w-1.5 rounded-full bg-red-400"></span>
            {{ q }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
