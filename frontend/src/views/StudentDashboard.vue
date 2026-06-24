<script setup>
import { computed, onMounted, ref } from "vue";

import KnowledgeGraph from "../components/KnowledgeGraph.vue";
import Navbar from "../components/Navbar.vue";
import Sidebar from "../components/Sidebar.vue";
import { useAnalyticsStore } from "../stores/analytics";
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
const analyticsStore = useAnalyticsStore();

const graphNodes = ref([
  { id: "basics" },
  { id: "derivatives" },
  { id: "integrals" },
  { id: "limits" },
  { id: "series" },
]);
const graphLinks = ref([
  { source: "basics", target: "limits" },
  { source: "limits", target: "derivatives" },
  { source: "derivatives", target: "integrals" },
  { source: "integrals", target: "series" },
]);

const courseProgress = ref(62);
const lessonsCompleted = ref(14);

const cognitiveLoadIndex = computed(() => analyticsStore.cognitiveLoadIndex);
const riskScore = computed(() => analyticsStore.riskScore?.risk_score || 0);

onMounted(() => {
  if (authStore.user?.id) {
    analyticsStore.fetchRiskScore(authStore.user.id);
  }
});

const metrics = computed(() => [
  { label: "Прогресс курса", value: `${courseProgress.value}%`, accent: "text-accent-light" },
  { label: "Когнитивная нагрузка", value: `${(cognitiveLoadIndex.value * 100).toFixed(0)}%`, accent: "text-orange-400" },
  { label: "Риск-скор", value: `${(riskScore.value * 100).toFixed(0)}%`, accent: "text-red-400" },
  { label: "Пройдено уроков", value: lessonsCompleted.value, accent: "text-green-400" },
]);
</script>

<template>
  <div class="flex min-h-screen bg-bg">
    <Sidebar />

    <div class="flex-1">
      <Navbar title="Главная" />

      <main class="space-y-6 p-6">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="metric in metrics" :key="metric.label" class="card p-5">
            <p class="text-sm text-text/60">{{ metric.label }}</p>
            <p :class="['mt-2 text-2xl font-bold', metric.accent]">{{ metric.value }}</p>
          </div>
        </div>

        <div class="card flex flex-col items-start gap-4 p-6 sm:flex-row sm:items-center sm:justify-between">
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
          <KnowledgeGraph :nodes="graphNodes" :links="graphLinks" />
        </div>
      </main>
    </div>
  </div>
</template>
