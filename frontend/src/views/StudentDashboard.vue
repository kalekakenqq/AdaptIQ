<script setup>
import axios from "axios";
import { computed, onMounted, ref } from "vue";

import KnowledgeGraph from "../components/KnowledgeGraph.vue";
import Navbar from "../components/Navbar.vue";
import Sidebar from "../components/Sidebar.vue";
import Skeleton from "../components/Skeleton.vue";
import { useAnalyticsStore } from "../stores/analytics";
import { useAuthStore } from "../stores/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const authStore = useAuthStore();
const analyticsStore = useAnalyticsStore();

const graphNodes = ref([]);
const graphEdges = ref([]);
const graphLoading = ref(true);
const loading = ref(true);

const courseProgress = ref(62);
const lessonsCompleted = ref(14);

const cognitiveLoadIndex = computed(() => analyticsStore.cognitiveLoadIndex);
const riskScore = computed(() => analyticsStore.riskScore?.risk_score || 0);

const metrics = computed(() => [
  { label: "Прогресс курса", value: `${courseProgress.value}%`, accent: "text-accent-light" },
  {
    label: "Когнитивная нагрузка",
    value: `${(cognitiveLoadIndex.value * 100).toFixed(0)}%`,
    accent: "text-orange-400",
  },
  { label: "Риск-скор", value: `${(riskScore.value * 100).toFixed(0)}%`, accent: "text-red-400" },
  { label: "Пройдено уроков", value: lessonsCompleted.value, accent: "text-green-400" },
]);

async function loadKnowledgeGraph() {
  graphLoading.value = true;
  try {
    const { data } = await axios.get(`${API_BASE_URL}/analytics/knowledge-graph`);
    graphNodes.value = data.nodes;
    graphEdges.value = data.edges;
  } catch (error) {
    console.error("Ошибка загрузки графа знаний:", error.response?.data ?? error.message);
  } finally {
    graphLoading.value = false;
  }
}

onMounted(async () => {
  if (authStore.user?.id) {
    await analyticsStore.fetchRiskScore(authStore.user.id);
  }
  loading.value = false;
  loadKnowledgeGraph();
});
</script>

<template>
  <div class="flex min-h-screen bg-bg">
    <Sidebar />

    <div class="flex-1">
      <Navbar title="Главная" />

      <main class="space-y-6 p-6">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <template v-if="loading">
            <Skeleton v-for="n in 4" :key="n" height="h-20" />
          </template>
          <template v-else>
            <div v-for="metric in metrics" :key="metric.label" class="card p-5">
              <p class="text-sm text-text/60">{{ metric.label }}</p>
              <p :class="['mt-2 text-2xl font-bold', metric.accent]">{{ metric.value }}</p>
            </div>
          </template>
        </div>

        <div
          class="card flex flex-col items-start gap-4 p-6 sm:flex-row sm:items-center sm:justify-between"
        >
          <div>
            <p class="text-sm text-text/60">Активный курс</p>
            <h2 class="mt-1 text-lg font-semibold text-text">Математический анализ</h2>
            <div class="mt-3 h-2 w-56 overflow-hidden rounded-full bg-white/10">
              <div
                class="h-full rounded-full bg-gradient-to-r from-accent to-accent-light"
                :style="{ width: `${courseProgress}%` }"
              ></div>
            </div>
          </div>
          <router-link
            to="/lesson/current"
            class="rounded-xl bg-gradient-to-r from-accent to-accent-light px-5 py-2.5 font-medium text-white shadow-lg transition-all duration-200 hover:brightness-110"
          >
            Продолжить
          </router-link>
        </div>

        <div>
          <h2 class="mb-3 text-sm font-medium text-text/70">Граф знаний</h2>
          <div v-if="graphLoading" class="card flex h-[420px] items-center justify-center">
            <div class="flex items-center gap-3 text-text/50">
              <svg class="h-5 w-5 animate-spin text-accent-light" viewBox="0 0 24 24" fill="none">
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                />
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 0 1 8-8V0C5.4 0 0 5.4 0 12h4Z"
                />
              </svg>
              Загрузка графа знаний...
            </div>
          </div>
          <KnowledgeGraph v-else :nodes="graphNodes" :edges="graphEdges" />
        </div>
      </main>
    </div>
  </div>
</template>
