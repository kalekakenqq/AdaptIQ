<script setup>
import axios from "axios";
import { Chart, registerables } from "chart.js";
import { onMounted, ref } from "vue";

import Navbar from "../components/Navbar.vue";
import Sidebar from "../components/Sidebar.vue";

Chart.register(...registerables);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const lessonId = ref("");
const summary = ref(null);
const chartCanvas = ref(null);

const groupStats = [
  { label: "Студентов в группе", value: 24 },
  { label: "Средний прогресс", value: "58%" },
  { label: "В зоне риска", value: 5 },
];

const students = ref([
  { name: "Анна Иванова", progress: "82%", risk: "low" },
  { name: "Пётр Смирнов", progress: "47%", risk: "medium" },
  { name: "Олег Кузнецов", progress: "19%", risk: "high" },
  { name: "Мария Соколова", progress: "91%", risk: "low" },
]);

function riskBadgeClass(risk) {
  if (risk === "low") return "bg-green-500/15 text-green-400";
  if (risk === "medium") return "bg-yellow-500/15 text-yellow-400";
  return "bg-red-500/15 text-red-400";
}

function riskLabel(risk) {
  if (risk === "low") return "Низкий";
  if (risk === "medium") return "Средний";
  return "Высокий";
}

async function loadSummary() {
  const response = await axios.get(`${API_BASE_URL}/reports/lesson/${lessonId.value}/summary`);
  summary.value = response.data;
}

onMounted(() => {
  new Chart(chartCanvas.value, {
    type: "line",
    data: {
      labels: ["Нед.1", "Нед.2", "Нед.3", "Нед.4", "Нед.5"],
      datasets: [
        {
          label: "Средний балл группы",
          data: [60, 64, 58, 70, 75],
          backgroundColor: "rgba(99,102,241,0.2)",
          borderColor: "#6366f1",
          fill: true,
          tension: 0.35,
        },
      ],
    },
    options: {
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
        y: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
      },
      plugins: { legend: { labels: { color: "#f1f5f9" } } },
    },
  });
});
</script>

<template>
  <div class="flex min-h-screen bg-bg">
    <Sidebar />

    <div class="flex-1">
      <Navbar title="Преподавателю" />

      <main class="space-y-6 p-6">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div v-for="stat in groupStats" :key="stat.label" class="card p-5">
            <p class="text-sm text-text/60">{{ stat.label }}</p>
            <p class="mt-2 text-2xl font-bold text-text">{{ stat.value }}</p>
          </div>
        </div>

        <div class="card p-5">
          <h2 class="mb-4 text-sm font-medium text-text/70">Динамика среднего балла</h2>
          <canvas ref="chartCanvas" height="90"></canvas>
        </div>

        <div class="card overflow-hidden">
          <table class="w-full text-left text-sm">
            <thead class="bg-white/5 text-text/60">
              <tr>
                <th class="px-5 py-3">Студент</th>
                <th class="px-5 py-3">Прогресс</th>
                <th class="px-5 py-3">Риск</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in students" :key="student.name" class="border-t border-white/5">
                <td class="px-5 py-3 text-text">{{ student.name }}</td>
                <td class="px-5 py-3 text-text/70">{{ student.progress }}</td>
                <td class="px-5 py-3">
                  <span :class="['rounded-full px-3 py-1 text-xs font-medium', riskBadgeClass(student.risk)]">
                    {{ riskLabel(student.risk) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="card space-y-3 p-5">
          <h2 class="text-sm font-medium text-text/70">Отчёт по уроку</h2>
          <div class="flex gap-2">
            <input v-model="lessonId" placeholder="ID урока" class="input-field" />
            <button
              class="whitespace-nowrap rounded-xl bg-gradient-to-r from-accent to-accent-light px-4 py-2.5 font-medium text-white transition-all duration-200 hover:brightness-110"
              @click="loadSummary"
            >
              Загрузить
            </button>
          </div>
          <div v-if="summary" class="text-sm text-text/70">
            <p>Количество сессий: {{ summary.sessions_count }}</p>
            <p>Средний балл: {{ summary.average_score.toFixed(2) }}</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
