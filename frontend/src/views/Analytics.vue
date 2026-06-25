<script setup>
import axios from "axios";
import { Chart, registerables } from "chart.js";
import { onBeforeUnmount, onMounted, ref } from "vue";

import Navbar from "../components/Navbar.vue";
import Sidebar from "../components/Sidebar.vue";

Chart.register(...registerables);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";
const DEMO_SESSION_ID = "00000000-0000-0000-0000-000000000001";

const CLUSTER_COLORS = ["#22c55e", "#6366f1", "#ef4444"];

const examChartRef = ref(null);
const clusterChartRef = ref(null);
const knowledgeChartRef = ref(null);
const factors = ref([]);
const loading = ref(true);

let examChart = null;
let clusterChart = null;
let knowledgeChart = null;

const darkScales = {
  x: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
  y: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
};

function knowledgeColor(value) {
  if (value > 0.7) return "rgba(34,197,94,0.6)";
  if (value >= 0.3) return "rgba(234,179,8,0.6)";
  return "rgba(239,68,68,0.6)";
}

async function loadExamPrediction() {
  const { data } = await axios.get(`${API_BASE_URL}/analytics/exam-prediction`);
  examChart = new Chart(examChartRef.value, {
    type: "line",
    data: {
      labels: data.weeks.map((week) => `Нед. ${week}`),
      datasets: [
        {
          label: "Вероятность сдачи экзамена, %",
          data: data.probability.map((p) => Math.round(p * 100)),
          backgroundColor: "rgba(99,102,241,0.2)",
          borderColor: "#6366f1",
          fill: true,
          tension: 0.35,
          pointBackgroundColor: "#818cf8",
        },
      ],
    },
    options: {
      scales: { ...darkScales, y: { ...darkScales.y, min: 0, max: 100 } },
      plugins: { legend: { labels: { color: "#f1f5f9" } } },
    },
  });
}

async function loadClusters() {
  const { data } = await axios.get(`${API_BASE_URL}/analytics/clusters`);
  const datasets = Object.entries(data.labels).map(([clusterId, label]) => ({
    label,
    data: data.clusters
      .filter((point) => point.cluster === Number(clusterId))
      .map((point) => ({ x: point.x, y: point.y, name: point.name })),
    backgroundColor: CLUSTER_COLORS[Number(clusterId) % CLUSTER_COLORS.length],
    pointRadius: 7,
    pointHoverRadius: 9,
  }));

  clusterChart = new Chart(clusterChartRef.value, {
    type: "scatter",
    data: { datasets },
    options: {
      scales: darkScales,
      plugins: {
        legend: { labels: { color: "#f1f5f9" } },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.raw.name} (${ctx.dataset.label})`,
          },
        },
      },
    },
  });
}

async function loadKnowledgeDistribution() {
  const { data } = await axios.get(`${API_BASE_URL}/analytics/knowledge-graph`);
  knowledgeChart = new Chart(knowledgeChartRef.value, {
    type: "bar",
    data: {
      labels: data.nodes.map((node) => node.label),
      datasets: [
        {
          label: "Уровень знания, %",
          data: data.nodes.map((node) => Math.round(node.knowledge * 100)),
          backgroundColor: data.nodes.map((node) => knowledgeColor(node.knowledge)),
          borderColor: "#6366f1",
          borderWidth: 1,
        },
      ],
    },
    options: {
      indexAxis: "y",
      scales: { ...darkScales, x: { ...darkScales.x, min: 0, max: 100 } },
      plugins: { legend: { labels: { color: "#f1f5f9" } } },
    },
  });
}

async function loadXai() {
  const { data } = await axios.get(`${API_BASE_URL}/analytics/xai-explanation/${DEMO_SESSION_ID}`);
  factors.value = data.factors;
}

onMounted(async () => {
  try {
    await Promise.all([
      loadExamPrediction(),
      loadClusters(),
      loadKnowledgeDistribution(),
      loadXai(),
    ]);
  } catch (error) {
    console.error("Ошибка загрузки аналитики:", error.response?.data ?? error.message);
  } finally {
    loading.value = false;
  }
});

onBeforeUnmount(() => {
  examChart?.destroy();
  clusterChart?.destroy();
  knowledgeChart?.destroy();
});
</script>

<template>
  <div class="flex min-h-screen bg-bg">
    <Sidebar />

    <div class="flex-1">
      <Navbar title="Аналитика" />

      <main class="space-y-6 p-6">
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div class="card p-5">
            <h2 class="mb-4 text-sm font-medium text-text/70">
              Прогноз результата экзамена (LSTM)
            </h2>
            <canvas ref="examChartRef" height="200"></canvas>
          </div>

          <div class="card p-5">
            <h2 class="mb-4 text-sm font-medium text-text/70">Кластеры студентов (UMAP)</h2>
            <canvas ref="clusterChartRef" height="200"></canvas>
          </div>
        </div>

        <div class="card p-5">
          <h2 class="mb-4 text-sm font-medium text-text/70">
            Распределение по уровням знаний
          </h2>
          <canvas ref="knowledgeChartRef" height="160"></canvas>
        </div>

        <div class="card p-5">
          <h2 class="mb-4 text-sm font-medium text-text/70">
            XAI: почему система выбрала этот материал
          </h2>
          <div class="space-y-3">
            <div v-for="factor in factors" :key="factor.name">
              <div class="mb-1 flex items-center justify-between text-sm">
                <span class="text-text/80">{{ factor.name }}</span>
                <span class="font-mono text-accent-light">{{ (factor.weight * 100).toFixed(0) }}%</span>
              </div>
              <div class="h-2 w-full overflow-hidden rounded-full bg-white/10">
                <div
                  class="h-full rounded-full bg-gradient-to-r from-accent to-accent-light"
                  :style="{ width: `${factor.weight * 100}%` }"
                ></div>
              </div>
            </div>
            <p v-if="!loading && factors.length === 0" class="text-sm text-text/40">
              Объяснения недоступны
            </p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
